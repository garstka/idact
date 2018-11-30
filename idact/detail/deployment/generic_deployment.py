"""This module contains the implementation of a generic deployment."""
from idact.core.retry import Retry
from idact.detail.helper.ptree import ptree
from idact.detail.helper.remove_runtime_dir import remove_runtime_dir_on_exit
from idact.detail.helper.retry import retry_with_config
from idact.detail.helper.stage_info import stage_debug
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_internal import NodeInternal
from idact.detail.serialization.serializable import Serializable
from idact.detail.serialization.serializable_types import SerializableTypes

CANCEL_TIMEOUT = 5


class GenericDeployment(Serializable):
    """Deployment of a program on a node.

        :param node: Node the program is running on.

        :param pid: Process id.

        :param output: Initial script output.

        :param runtime_dir: Runtime dir to remove.

    """

    def __init__(self,
                 node: NodeInternal,
                 pid: int,
                 runtime_dir: str):
        self._node = node
        self._pid = pid
        self._runtime_dir = runtime_dir

    @property
    def node(self) -> NodeInternal:
        """Node the program is running on."""
        return self._node

    @property
    def pid(self) -> int:
        """Deployed program pid."""
        return self._pid

    def cancel(self):
        """Kills the program and all its child processes.
            Removes the runtime dir.
            Raises an exception if the top level process is still running
            after :attr:`.CANCEL_TIMEOUT` seconds.

            :raises RuntimeError: If the program is still running.

        """

        parent_pid = self._pid
        node = self._node

        def cancel_task():
            """Kills a list of processes, waits and fails if all are still
                running after a timeout."""
            tree = ' '.join([str(pid)
                             for pid
                             in ptree(pid=parent_pid, node=node)])
            node.run(
                "kill {tree}"
                "; sleep {timeout}"
                "; kill -0 {pid} && exit 1 || exit 0".format(
                    tree=tree,
                    pid=self._pid,
                    timeout=CANCEL_TIMEOUT))

        log = get_logger(__name__)
        with remove_runtime_dir_on_exit(node=self._node,
                                        runtime_dir=self._runtime_dir):
            with stage_debug(log,
                             "Killing the process tree for pid: %d",
                             self._pid):
                retry_with_config(fun=cancel_task,
                                  name=Retry.CANCEL_DEPLOYMENT,
                                  config=self._node.config)

    def serialize(self) -> dict:
        return {'type': str(SerializableTypes.GENERIC_DEPLOYMENT),
                'node': self._node.serialize(),
                'pid': self._pid,
                'runtime_dir': self._runtime_dir}

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
