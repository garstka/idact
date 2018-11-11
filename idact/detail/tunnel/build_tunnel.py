"""This module contains a function that builds an SSH tunnel."""
from contextlib import ExitStack
from typing import List, Optional

from sshtunnel import SSHTunnelForwarder

from idact.core.tunnel import Tunnel
from idact.detail.helper.retry import retry
from idact.detail.helper.stage_info import stage_debug
from idact.detail.log.get_logger import get_logger, get_debug_logger
from idact.detail.tunnel.binding import Binding
from idact.detail.tunnel.close_tunnel_on_failure import close_tunnel_on_failure
from idact.detail.tunnel.first_hop_tunnel import FirstHopTunnel
from idact.detail.tunnel.multi_hop_tunnel import MultiHopTunnel

ANY_ADDRESS = ("", 0)
TUNNEL_KEEPALIVE = 30.0
TUNNEL_RETRIES = 3
TUNNEL_RETRY_INTERVAL = 5


# pylint: disable=too-many-locals
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

    with ExitStack() as stack:
        tunnels = []

        log = get_logger(__name__)
        log.debug("Ssh username: %s", ssh_username)
        log.debug("Using password: %r", ssh_password is not None)
        log.debug("Using key file: %s", ssh_pkey)

        logger = get_debug_logger("{}/Tunnels".format(__name__))

        # First hop if not the only one
        if len(bindings) != 2:
            with stage_debug(log, "Adding first hop."):
                ssh_address_or_host = (hostname, port)
                local_bind_address = ANY_ADDRESS
                remote_bind_address = bindings[1].as_tuple()
                log.debug("Ssh address is %s", ssh_address_or_host)
                log.debug("Local bind address is %s", local_bind_address)
                log.debug("Remote bind address is %s", remote_bind_address)

                def create_first_tunnel():
                    return FirstHopTunnel(
                        forwarder=SSHTunnelForwarder(
                            ssh_address_or_host,
                            ssh_config_file=None,
                            ssh_username=ssh_username,
                            ssh_password=ssh_password,
                            ssh_pkey=ssh_pkey,
                            local_bind_address=local_bind_address,
                            remote_bind_address=remote_bind_address,
                            set_keepalive=TUNNEL_KEEPALIVE,
                            allow_agent=False,
                            logger=logger),
                        there=bindings[1].port)

                tunnel = retry(create_first_tunnel,
                               retries=TUNNEL_RETRIES,
                               seconds_between_retries=TUNNEL_RETRY_INTERVAL)
                stack.enter_context(close_tunnel_on_failure(tunnel))
                tunnels.append(tunnel)

        # Middle hops if any
        prev_tunnel = tunnels[0] if tunnels else None
        for i, next_binding in enumerate(bindings[2:-1]):
            with stage_debug(log, "Adding middle hop %d.", i):
                # Connect through previous tunnel
                ssh_address_or_host = (
                    "127.0.0.1",
                    prev_tunnel.forwarder.local_bind_port)
                local_bind_address = ANY_ADDRESS
                remote_bind_address = next_binding.as_tuple()
                log.debug("Ssh address is %s", ssh_address_or_host)
                log.debug("Local bind address is %s", local_bind_address)
                log.debug("Remote bind address is %s", remote_bind_address)
                next_binding_port = next_binding.port

                def create_middle_tunnel():
                    return FirstHopTunnel(
                        forwarder=SSHTunnelForwarder(
                            ssh_address_or_host,
                            ssh_config_file=None,
                            ssh_username=ssh_username,
                            ssh_password=ssh_password,
                            ssh_pkey=ssh_pkey,
                            local_bind_address=local_bind_address,
                            remote_bind_address=remote_bind_address,
                            set_keepalive=TUNNEL_KEEPALIVE,
                            allow_agent=False,
                            logger=logger),
                        there=next_binding_port)  # noqa, pylint: disable=cell-var-from-loop, line-too-long

                next_tunnel = retry(
                    create_middle_tunnel,
                    retries=TUNNEL_RETRIES,
                    seconds_between_retries=TUNNEL_RETRY_INTERVAL)
                stack.enter_context(close_tunnel_on_failure(next_tunnel))
                tunnels.append(next_tunnel)
                prev_tunnel = next_tunnel

        with stage_debug(log, "Adding last hop."):
            # Last hop
            last_hop_port = (port
                             if len(bindings) == 2
                             else tunnels[-1].forwarder.local_bind_port)

            ssh_address_or_host = ("127.0.0.1", last_hop_port)
            local_bind_address = bindings[0].as_tuple()
            remote_bind_address = bindings[-1].as_tuple()
            log.debug("Ssh address is %s", ssh_address_or_host)
            log.debug("Local bind address is %s", local_bind_address)
            log.debug("Remote bind address is %s", remote_bind_address)

            def create_last_tunnel():
                return FirstHopTunnel(
                    forwarder=SSHTunnelForwarder(
                        ssh_address_or_host,
                        ssh_config_file=None,
                        ssh_username=ssh_username,
                        ssh_password=ssh_password,
                        ssh_pkey=ssh_pkey,
                        local_bind_address=local_bind_address,
                        remote_bind_address=remote_bind_address,
                        set_keepalive=TUNNEL_KEEPALIVE,
                        allow_agent=False,
                        logger=logger),
                    there=bindings[-1].port)

            last_tunnel = retry(
                create_last_tunnel,
                retries=TUNNEL_RETRIES,
                seconds_between_retries=TUNNEL_RETRY_INTERVAL)
            stack.enter_context(close_tunnel_on_failure(last_tunnel))
            tunnels.append(last_tunnel)

        if len(tunnels) == 1:
            return tunnels[0]
        return MultiHopTunnel(tunnels=tunnels)
