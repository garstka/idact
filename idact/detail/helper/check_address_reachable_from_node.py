from idact.core.nodes import Node


def check_address_reachable_from_node(node: Node,
                                      ip_address: str,
                                      port: int):
    """Attempts to connect to this address from node using TCP.

        :param node:        Node to test the connection from.
        :param ip_address:  Ip address to connect to.
        :param port:        Port to connect to.

    """
    node.run("python -c 'import socket; s=socket.socket("
             "socket.AF_INET, socket.SOCK_STREAM);"
             " s.connect((\"{ip_address}\", {port})); "
             " s.close()'".format(ip_address=ip_address,
                                  port=port))
