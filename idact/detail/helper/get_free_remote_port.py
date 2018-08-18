"""This module contains functions for obtaining free port numbers
    on a cluster."""

from typing import List

from idact.core.nodes import Node


def get_free_remote_port(node: Node) -> int:
    """Returns a free remote port.

        Uses a Python snippet to determine a free port by binding a socket
        to port 0 and immediately releasing it.

        :param node: Node to find a port on.

    """
    output = node.run("python -c 'import socket; s=socket.socket();"
                      " s.bind((str(), 0)); print(s.getsockname()[1]);"
                      " s.close()'")
    return int(output)


def get_free_remote_ports(count: int, node: Node) -> List[int]:
    """Returns several free remote ports.

        See :func:`.get_free_remote_port`.

        :param count: Free port count.

        :param node: Node to find a port on.

    """

    result = {get_free_remote_port(node=node) for _ in range(count)}

    if len(result) != count:
        raise RuntimeError(
            "Unable to obtain free ports on node, count: '{}'.".format(count))
    return list(result)
