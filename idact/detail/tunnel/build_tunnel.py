"""This module contains a function that builds an SSH tunnel."""
from typing import List, Optional

from sshtunnel import SSHTunnelForwarder

from idact.core.tunnel import Tunnel
from idact.detail.helper.stage_info import stage_debug
from idact.detail.log.get_logger import get_logger
from idact.detail.tunnel.binding import Binding
from idact.detail.tunnel.first_hop_tunnel import FirstHopTunnel
from idact.detail.tunnel.multi_hop_tunnel import MultiHopTunnel

ANY_ADDRESS = ("", 0)
TUNNEL_KEEPALIVE = 30.0


def build_tunnel(bindings: List[Binding],
                 hostname: str,
                 port: int,
                 ssh_username: str,
                 ssh_password: Optional[str] = None,
                 ssh_pkey: Optional[str] = None) -> Tunnel:
    """Builds a multi-hop tunnel from a sequence of bindings.

        :param hostname: First host name.

        :param port:     First host SSH port.

        :param bindings: Sequence of bindings, starting with the local binding.

        :param ssh_username: Ssh username.

        :param ssh_password: Ssh password.

        :param ssh_pkey: Ssh private key.
    """
    if len(bindings) < 2:
        raise ValueError("At least one local and one remote binding"
                         " is required to build a tunnel")

    tunnels = []

    log = get_logger(__name__)
    # First hop if not the only one
    if len(bindings) != 2:
        with stage_debug(log, "Adding first hop."):
            tunnels.append(FirstHopTunnel(
                forwarder=SSHTunnelForwarder(
                    (hostname, port),
                    ssh_config_file=None,
                    ssh_username=ssh_username,
                    ssh_password=ssh_password,
                    ssh_pkey=ssh_pkey,
                    local_bind_address=ANY_ADDRESS,
                    remote_bind_address=bindings[1].as_tuple(),
                    set_keepalive=TUNNEL_KEEPALIVE,
                    allow_agent=False),
                there=bindings[1].port))

    # Middle hops if any
    prev_tunnel = tunnels[0] if tunnels else None
    for i, next_binding in enumerate(bindings[2:-1]):
        with stage_debug(log, "Adding middle hop %d.", i):
            # Connect through previous tunnel
            next_tunnel = \
                FirstHopTunnel(
                    forwarder=SSHTunnelForwarder(
                        ("127.0.0.1", prev_tunnel.forwarder.local_bind_port),
                        ssh_config_file=None,
                        ssh_username=ssh_username,
                        ssh_password=ssh_password,
                        ssh_pkey=ssh_pkey,
                        local_bind_address=ANY_ADDRESS,
                        remote_bind_address=next_binding.as_tuple(),
                        set_keepalive=TUNNEL_KEEPALIVE,
                        allow_agent=False),
                    there=next_binding.port)
            tunnels.append(next_tunnel)
            prev_tunnel = next_tunnel

    with stage_debug(log, "Adding last hop."):
        # Last hop
        last_hop_port = (port
                         if len(bindings) == 2
                         else tunnels[-1].forwarder.local_bind_port)

        tunnels.append(FirstHopTunnel(
            forwarder=SSHTunnelForwarder(
                ("127.0.0.1", last_hop_port),
                ssh_config_file=None,
                ssh_username=ssh_username,
                ssh_password=ssh_password,
                ssh_pkey=ssh_pkey,
                local_bind_address=bindings[0].as_tuple(),
                remote_bind_address=bindings[-1].as_tuple(),
                set_keepalive=TUNNEL_KEEPALIVE,
                allow_agent=False),
            there=bindings[-1].port))

    if len(tunnels) == 1:
        return tunnels[0]
    return MultiHopTunnel(tunnels=tunnels)
