from idact.core.nodes import Node
from idact.detail.helper.ptree import ptree

CANCEL_TIMEOUT = 5


class GenericDeployment:
    """Deployment of a program on a node.

        :param node: Node the program is running on.

        :param pid: Process id.

    """

    def __init__(self,
                 node: Node,
                 pid: int,
                 output: str):
        self._node = node
        self._pid = pid
        self._output = output

    @property
    def pid(self) -> int:
        """Deployed program pid."""
        return self._pid

    @property
    def output(self) -> str:
        """Console output after running the program."""
        return self._output

    def cancel(self):
        """Kills the program and all its child processes.
           Fails, if the top level process is still running after timeout.
        """
        tree = ' '.join([str(pid)
                         for pid
                         in ptree(pid=self._pid, node=self._node)])
        self._node.run(
            "kill {tree}"
            "; sleep {timeout}"
            "; kill -0 {pid} && exit 1 || exit 0".format(
                tree=tree,
                pid=self._pid,
                timeout=CANCEL_TIMEOUT))
