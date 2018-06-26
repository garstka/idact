import datetime
from typing import Optional

import fabric.operations
import fabric.tasks
import fabric.decorators

from idact.core.nodes import Node
from idact.detail.auth.authenticate import authenticate
from idact.detail.config.client.client_cluster_config \
    import ClientClusterConfig
from idact.detail.helper.raise_on_remote_fail import raise_on_remote_fail
from idact.detail.helper.utc_now import utc_now


class NodeImpl(Node):
    """Cluster node interface.

        :param config: Client cluster config.

        :param access_node: Main cluster node that does not require allocation,
                            or None if this node is an access node.
    """

    def __init__(self,
                 config: ClientClusterConfig):
        self._config = config
        self._host: Optional[str] = None
        self._allocated_until: Optional[datetime.datetime] = None

    def run(self, command: str) -> str:
        """Runs a command on the node and returns the output.

            :param command: Command to run.
        """

        if self._allocated_until and self._allocated_until < utc_now():
            message = ("Cannot run '{command}'. "
                       "'{node}' was terminated at '{timestamp}'.")
            raise RuntimeError(message.format(
                command=command,
                node=self._host,
                timestamp=self._allocated_until.isoformat()))
        if self._host is None:
            message = "Cannot run '{command}'. Node is not allocated."
            raise RuntimeError(message.format(command=command))

        @fabric.decorators.task
        def task():
            return fabric.operations.run(command)

        with raise_on_remote_fail(exception=RuntimeError):
            with authenticate(host=self._host, config=self._config):
                result = fabric.tasks.execute(task)

        output = next(iter(result.values()))
        return output

    def make_allocated(self,
                       host: str,
                       allocated_until: Optional[datetime.datetime]):
        """Updates the allocation info.

            :param host: Hostname of the cluster node.

            :param allocated_until: Timestamp for job termination. Must be UTC
                                    or contain timezone info.
                                    None is treated as unlimited allocation.
        """
        self._host = host
        self._allocated_until = allocated_until

    def make_cancelled(self):
        """Updates the allocation info after the allocation was cancelled."""
        self._host = None
        self._allocated_until = None

    def __str__(self):
        return "Node({host}, {allocated_until})".format(
            host=self._host,
            allocated_until=self._allocated_until)
