"""This module contains a function for listing a process tree recursively."""

from typing import List

from idact.core.nodes import Node

# https://unix.stackexchange.com/questions/124127/kill-all-descendant-processes
LIST_DESCENDANTS = (
    r'list_descendants () {'
    r' local children=$(pgrep -P "$1");'
    r' for pid in $children;'
    r' do list_descendants "$pid";'
    r' done;'
    r' echo "$children"; }')


def ptree(pid: int, node: Node) -> List[int]:
    """Returns a list containing this PID and all its descendants.

        :param pid: Parent process pid.

        :param node: Node to run pgrep on.

    """
    result = node.run(
        "{list_descendants};"
        " echo $(list_descendants {pid})".format(
            list_descendants=LIST_DESCENDANTS,
            pid=pid))
    if not result:
        return [pid]
    descendant_pids = [int(descendant_pid)
                       for descendant_pid in result.split(' ')]

    return [pid] + descendant_pids
