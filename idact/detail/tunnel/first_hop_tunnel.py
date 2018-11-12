"""This module contains the implementation of a single hop SSH tunnel."""

from sshtunnel import SSHTunnelForwarder

from idact.core.config import ClusterConfig
from idact.detail.tunnel.tunnel_internal import TunnelInternal


class FirstHopTunnel(TunnelInternal):
    """Direct tunnel to the gateway, or any node accessible from localhost.
        Uses pure Python tunneling with `sshtunnel`.

        :param forwarder: `sshtunnel` forwarder.

        :param there: Remote binding port.

    """

    def __init__(self,
                 forwarder: SSHTunnelForwarder,
                 there: int,
                 config: ClusterConfig):
        self._forwarder = forwarder
        self._there = there

        self._forwarder.start()
        self._here = forwarder.local_bind_address[1]

        self._config = config

    @property
    def there(self) -> int:
        return self._there

    @property
    def here(self) -> int:
        return self._here

    def close(self):
        self._forwarder.stop()

    @property
    def forwarder(self) -> SSHTunnelForwarder:
        """SSH tunnel forwarder from the :mod:`sshtunnel` module."""
        return self._forwarder

    @property
    def config(self) -> ClusterConfig:
        return self._config
