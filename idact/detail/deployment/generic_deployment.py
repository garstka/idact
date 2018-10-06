"""This module contains the implementation of a generic deployment."""

from idact.core.nodes import Node
from idact.detail.helper.ptree import ptree
from idact.detail.helper.remove_runtime_dir import remove_runtime_dir_on_exit
from idact.detail.helper.retry import retry
from idact.detail.helper.stage_info import stage_debug
from idact.detail.log.get_logger import get_logger

CANCEL_TIMEOUT = 5


class GenericDeployment:
    """Deployment of a program on a node.

        :param node: Node the program is running on.

        :param pid: Process id.

        :param runtime_dir: Runtime dir to remove.

    """

    def __init__(self,
                 node: Node,
                 pid: int,
                 output: str,
                 runtime_dir: str):
        self._node = node
        self._pid = pid
        self._output = output
        self._runtime_dir = runtime_dir

    @property
    def node(self) -> Node:
        """Node the program is running on."""
        return self._node

    @property
    def pid(self) -> int:
        """Deployed program pid."""
        return self._pid

    @property
    def output(self) -> str:
        """Console output captured for a few seconds after running
            the program.
        """
        return self._output

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
                retry(fun=cancel_task,
                      retries=5,
                      seconds_between_retries=1)
