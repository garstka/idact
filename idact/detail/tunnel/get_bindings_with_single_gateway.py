from typing import List

from idact.detail.tunnel.binding import Binding

LOCAL_BINDING_ADDRESS = ""
REMOTE_BINDING_ADDRESS = "127.0.0.1"


def get_bindings_with_single_gateway(here: int,
                                     node_host: str,
                                     node_port: int,
                                     there: int) -> List[Binding]:
    """Returns bindings for a tunnel through a single gateway.

        :param here: Local port number.

        :param node_host: Node hostname from the gateway.

        :param node_port: Node SSH port from the gateway.

        :param there: Remote port number.

        """
    return [Binding(LOCAL_BINDING_ADDRESS, here),
            Binding(node_host, node_port),
            Binding(REMOTE_BINDING_ADDRESS, there)]
