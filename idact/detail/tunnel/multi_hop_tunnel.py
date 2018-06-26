from typing import List

from idact.core.tunnel import Tunnel


class MultiHopTunnel(Tunnel):
    """Tunnel consisting of multiple segments.

        :param tunnels: Tunnel segements, at least one.
    """

    def __init__(self, tunnels: List[Tunnel]):
        if not tunnels:
            raise ValueError(
                "Multi-hop tunnel requires at least one tunnel segment.")
        self._tunnels = tunnels
        self._here = tunnels[-1].here
        self._there = tunnels[-1].there

    @property
    def there(self) -> int:
        return self._there

    @property
    def here(self) -> int:
        return self._here

    def close(self):
        for i in reversed(self._tunnels):
            i.close()
