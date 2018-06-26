from typing import List, Optional

from sshtunnel import SSHTunnelForwarder

from idact.core.tunnel import Tunnel
from idact.detail.tunnel.binding import Binding
from idact.detail.tunnel.first_hop_tunnel import FirstHopTunnel
from idact.detail.tunnel.multi_hop_tunnel import MultiHopTunnel

ANY_ADDRESS = ("", 0)


def build_tunnel(bindings: List[Binding],
                 hostname: str,
                 port: int,
                 ssh_username: str,
                 ssh_password: Optional[str]) -> Tunnel:
    """Builds a multi-hop tunnel from a sequence of bindings.

        :param hostname: First host name.

        :param port:     First host SSH port.

        :param bindings: Sequence of bindings, starting with the local binding.

        :param ssh_username: Ssh username for the first hop.

        :param ssh_password: Ssh password for the first hop.
    """
    if len(bindings) < 2:
        raise ValueError("At least one local and one remote binding"
                         " is required to build a tunnel")

    tunnels = []

    # First hop if not the only one
    if len(bindings) != 2:
        tunnels.append(FirstHopTunnel(
            forwarder=SSHTunnelForwarder(
                (hostname, port),
                ssh_username=ssh_username,
                ssh_password=ssh_password,
                local_bind_address=ANY_ADDRESS,
                remote_bind_address=bindings[1].as_tuple()),
            there=bindings[1].port))

    # Middle hops if any
    prev_tunnel = tunnels[0] if tunnels else None
    for next_binding in bindings[2:-1]:
        # Connect through previous tunnel
        next_tunnel = \
            FirstHopTunnel(
                forwarder=SSHTunnelForwarder(
                    ("127.0.0.1", prev_tunnel.forwarder.local_bind_port),
                    ssh_username=ssh_username,
                    ssh_password=ssh_password,
                    local_bind_address=ANY_ADDRESS,
                    remote_bind_address=next_binding.as_tuple()),
                there=next_binding.port)

        tunnels.append(next_tunnel)
        prev_tunnel = next_tunnel

    # Last hop
    last_hop_port = (port
                     if len(bindings) == 2
                     else tunnels[-1].forwarder.local_bind_port)

    tunnels.append(FirstHopTunnel(
        forwarder=SSHTunnelForwarder(
            ("127.0.0.1", last_hop_port),
            ssh_username=ssh_username,
            ssh_password=ssh_password,
            local_bind_address=bindings[0].as_tuple(),
            remote_bind_address=bindings[-1].as_tuple()),
        there=bindings[-1].port))

    if len(tunnels) == 1:
        return tunnels[0]
    return MultiHopTunnel(tunnels=tunnels)
