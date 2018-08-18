"""This module contains a function for listing a process tree recursively."""

from typing import List

from idact.core.nodes import Node


def ptree(pid: int, node: Node) -> List[int]:
    """Returns a list containing this PID and all its offspring, by running
        `pgrep` repeatedly.

        :param pid: Parent process pid.

        :param node: Node to run pgrep on.

    """
    result = node.run("pgrep -P {pid}; exit 0".format(pid=pid))
    if not result:
        return [pid]
    child_pids = [int(child_pid)
                  for child_pid in result.splitlines()]

    rest = [ptree(child_pid, node)
            for child_pid in child_pids]

    rest_flat = [y for x in rest
                 for y in x]

    return [pid] + rest_flat
