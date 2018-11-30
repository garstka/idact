"""This module contains the implementation of the cluster node interface."""

import datetime
from typing import Optional, Any, Callable

import bitmath
import fabric.operations
import fabric.tasks
import fabric.decorators
from fabric.exceptions import CommandTimeout
from fabric.state import env

from idact.core.retry import Retry
from idact.core.config import ClusterConfig
from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.node_resource_status import NodeResourceStatus
from idact.detail.auth.authenticate import authenticate
from idact.detail.helper.raise_on_remote_fail import raise_on_remote_fail
from idact.detail.helper.retry import retry_with_config
from idact.detail.helper.stage_info import stage_debug
from idact.detail.helper.utc_from_str import utc_from_str
from idact.detail.helper.utc_now import utc_now
from idact.detail.jupyter.deploy_jupyter import deploy_jupyter
from idact.detail.log.capture_fabric_output_to_log import \
    capture_fabric_output_to_log
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_internal import NodeInternal
from idact.detail.nodes.node_resource_status_impl import NodeResourceStatusImpl
from idact.detail.serialization.serializable_types import SerializableTypes
from idact.detail.tunnel.build_tunnel import build_tunnel
from idact.detail.tunnel.get_bindings_with_single_gateway import \
    get_bindings_with_single_gateway
from idact.detail.tunnel.ssh_tunnel import SshTunnel
from idact.detail.tunnel.tunnel_internal import TunnelInternal
from idact.detail.tunnel.validate_tunnel_ports import validate_tunnel_ports

ANY_TUNNEL_PORT = 0


class NodeImpl(NodeInternal):
    """Implementation of cluster node interface.

        :param config: Client cluster config.

    """

    def connect(self, timeout: Optional[int] = None):
        result = self.run("echo 'Testing connection...'", timeout=timeout)
        if result != 'Testing connection...':
            raise RuntimeError("Unexpected test command output.")

    def __init__(self,
                 config: ClusterConfig):
        self._config = config
        self._host = None  # type: Optional[str]
        self._port = None  # type: Optional[int]
        self._cores = None  # type: Optional[int]
        self._memory = None  # type: Optional[bitmath.Byte]
        self._allocated_until = None  # type: Optional[datetime.datetime]

    def _ensure_allocated(self):
        """Raises an exception if the node is not allocated."""
        if self._host is None:
            raise RuntimeError("Node is not allocated.")
        if self._allocated_until and self._allocated_until < utc_now():
            message = "'{node}' was terminated at '{timestamp}'."
            raise RuntimeError(message.format(
                node=self._host,
                timestamp=self._allocated_until.isoformat()))

    def run(self,
            command: str,
            timeout: Optional[int] = None) -> str:
        return self.run_impl(command=command,
                             timeout=timeout,
                             install_keys=False)

    def run_impl(self,
                 command: str,
                 timeout: Optional[int] = None,
                 install_keys: bool = False) -> str:
        try:
            @fabric.decorators.task
            def task():
                """Runs the command with a timeout."""
                with capture_fabric_output_to_log():
                    return fabric.operations.run(command,
                                                 pty=False,
                                                 timeout=timeout)

            return self.run_task(task=task,
                                 install_keys=install_keys)
        except CommandTimeout as e:
            raise TimeoutError("Command timed out: '{command}'".format(
                command=command)) from e
        except RuntimeError as e:
            raise RuntimeError("Cannot run '{command}'".format(
                command=command)) from e

    def run_task(self,
                 task: Callable,
                 install_keys: bool = False) -> Any:
        try:
            self._ensure_allocated()

            with raise_on_remote_fail(exception=RuntimeError):
                with authenticate(host=self._host,
                                  port=self._port,
                                  config=self._config,
                                  install_shared_keys=install_keys):
                    result = fabric.tasks.execute(task)

            output = next(iter(result.values()))

            return output
        except RuntimeError as e:
            raise RuntimeError("Cannot run task.") from e

    def make_allocated(self,
                       host: str,
                       port: int,
                       cores: Optional[int],
                       memory: Optional[bitmath.Byte],
                       allocated_until: Optional[datetime.datetime]):
        """Updates the allocation info.

            :param host: Hostname of the cluster node.

            :param port: SSH port of the cluster node.

            :param cores: Allocated core count.

            :param memory: Allocated memory.

            :param allocated_until: Timestamp for job termination. Must be UTC
                                    or contain timezone info.
                                    None is treated as unlimited allocation.

        """
        self._host = host
        self._port = port
        self._cores = cores
        self._memory = memory
        self._allocated_until = allocated_until

    def make_cancelled(self):
        """Updates the allocation info after the allocation was cancelled."""
        self._host = None
        self._port = None
        self._cores = None
        self._memory = None
        self._allocated_until = None

    def __str__(self):
        if not self._host:
            return "Node(NotAllocated)"
        return "Node({host}:{port}, {allocated_until})".format(
            host=self._host,
            port=self._port,
            allocated_until=self._allocated_until)

    def __repr__(self):
        return str(self)

    def tunnel(self,
               there: int,
               here: Optional[int] = None) -> TunnelInternal:
        try:
            log = get_logger(__name__)
            with stage_debug(log, "Opening tunnel %s -> %d to %s",
                             here, there, self):
                self._ensure_allocated()

                here, there = validate_tunnel_ports(here=here,
                                                    there=there)

                first_try = [True]

                def get_bindings_and_build_tunnel() -> TunnelInternal:
                    bindings = get_bindings_with_single_gateway(
                        here=here if first_try[0] else ANY_TUNNEL_PORT,
                        node_host=self._host,
                        node_port=self._port,
                        there=there)
                    first_try[0] = False
                    return build_tunnel(config=self._config,
                                        bindings=bindings,
                                        ssh_password=env.password,
                                        ssh_pkey=env.key_filename)

                with authenticate(host=self._host,
                                  port=self._port,
                                  config=self._config):
                    if here == ANY_TUNNEL_PORT:
                        return get_bindings_and_build_tunnel()
                    return retry_with_config(
                        get_bindings_and_build_tunnel,
                        name=Retry.TUNNEL_TRY_AGAIN_WITH_ANY_PORT,
                        config=self._config)

        except RuntimeError as e:
            raise RuntimeError(
                "Unable to tunnel {there} on node '{host}'.".format(
                    there=there,
                    host=self._host)) from e

    def tunnel_ssh(self,
                   here: Optional[int] = None) -> TunnelInternal:
        return SshTunnel(tunnel=self.tunnel(here=self.port, there=self.port))

    def deploy_notebook(self, local_port: int = 8080) -> JupyterDeployment:
        return deploy_jupyter(node=self,
                              local_port=local_port)

    @property
    def config(self) -> ClusterConfig:
        return self._config

    @property
    def host(self) -> Optional[str]:
        return self._host

    @property
    def port(self) -> Optional[int]:
        return self._port

    @property
    def cores(self) -> Optional[int]:
        return self._cores

    @property
    def memory(self) -> Optional[bitmath.Byte]:
        return self._memory

    @property
    def resources(self) -> NodeResourceStatus:
        return NodeResourceStatusImpl(node=self)

    def serialize(self) -> dict:
        return {'type': str(SerializableTypes.NODE_IMPL),
                'host': self._host,
                'port': self._port,
                'cores': self._cores,
                'memory': (None if self._memory is None
                           else str(self._memory)),
                'allocated_until': (None if self._allocated_until is None
                                    else self._allocated_until.isoformat())}

    @staticmethod
    def deserialize(config: ClusterConfig, serialized: dict) -> 'NodeImpl':
        try:
            assert serialized['type'] == str(SerializableTypes.NODE_IMPL)
            node = NodeImpl(config=config)
            node.make_allocated(
                host=serialized['host'],
                port=serialized['port'],
                cores=serialized['cores'],
                memory=(None if serialized['memory'] is None
                        else bitmath.parse_string(serialized['memory'])),
                allocated_until=(
                    None if serialized['allocated_until'] is None
                    else utc_from_str(serialized['allocated_until'])))
            return node
        except KeyError as e:
            raise RuntimeError("Unable to deserialize.") from e

    @property
    def allocated_until(self) -> Optional[datetime.datetime]:
        return self._allocated_until

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
