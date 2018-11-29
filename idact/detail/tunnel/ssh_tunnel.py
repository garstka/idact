from idact.core.config import ClusterConfig
from idact.detail.tunnel.tunnel_internal import TunnelInternal


class SshTunnel(TunnelInternal):
    """Wrapper for a tunnel that returns a formatted ssh command on str().

        :param tunnel: Tunnel to wrap.

    """

    def __init__(self,
                 tunnel: TunnelInternal):
        self._tunnel = tunnel

    @property
    def there(self) -> int:
        return self._tunnel.there

    @property
    def here(self) -> int:
        return self._tunnel.here

    def close(self):
        return self._tunnel.close()

    def __str__(self):
        return 'ssh -i "{key}" -p {here} {user}@localhost'.format(
            key=self._tunnel.config.key,
            here=self._tunnel.here,
            user=self.config.user)

    def __repr__(self):
        return str(self)

    @property
    def config(self) -> ClusterConfig:
        return self._tunnel.config
