from idact.core.nodes import Node
from idact.detail.helper.ptree import ptree
from idact.detail.helper.remove_runtime_dir import remove_runtime_dir_on_exit
from idact.detail.helper.retry import retry

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

        def cancel_task():
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

        with remove_runtime_dir_on_exit(node=self._node,
                                        runtime_dir=self._runtime_dir):
            retry(fun=cancel_task,
                  retries=5,
                  seconds_between_retries=1)
