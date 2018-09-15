"""This module contains the implementation of the cluster node interface."""

import datetime
from typing import Optional, Any, Callable

import bitmath
import fabric.operations
import fabric.tasks
import fabric.decorators
from fabric.exceptions import CommandTimeout
from fabric.state import env

from idact.core.config import ClusterConfig
from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.node_resource_status import NodeResourceStatus
from idact.detail.auth.authenticate import authenticate
from idact.detail.config.validation.validate_port import validate_port
from idact.detail.helper.raise_on_remote_fail import raise_on_remote_fail
from idact.detail.helper.utc_now import utc_now
from idact.detail.jupyter.deploy_jupyter import deploy_jupyter
from idact.detail.nodes.node_internal import NodeInternal
from idact.detail.nodes.node_resource_status_impl import NodeResourceStatusImpl
from idact.detail.tunnel.binding import Binding
from idact.detail.tunnel.build_tunnel import build_tunnel


class NodeImpl(NodeInternal):
    """Implementation of cluster node interface.

        :param config: Client cluster config.

    """

    def __init__(self,
                 config: ClusterConfig):
        self._config = config
        self._host = None  # type: Optional[str]
        self._port = None  # type: Optional[int]
        self._cores = None  # type: Optional[int]
        self._memory = None  # type: Optional[int]
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
               here: Optional[int] = None):
        try:
            here = here if here is not None else 0
            validate_port(there)
            if here != 0:
                validate_port(here)

            self._ensure_allocated()

            bindings = [Binding("", here),
                        Binding(self._host, self._port),
                        Binding("127.0.0.1", there)]

            with authenticate(host=self._host,
                              port=self._port,
                              config=self._config):
                return build_tunnel(bindings=bindings,
                                    hostname=self._config.host,
                                    port=self._config.port,
                                    ssh_username=self._config.user,
                                    ssh_password=env.password,
                                    ssh_pkey=env.key_filename)
        except RuntimeError as e:
            raise RuntimeError(
                "Unable to tunnel {there} on node '{host}'.".format(
                    there=there,
                    host=self._host)) from e

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
