from idact import ClusterConfig
from idact.detail.tunnel.tunnel_internal import TunnelInternal


class FakeTunnel(TunnelInternal):
    """Does nothing besides holding the remote port.
        Local port is ignored.

        :param there: Remote port.

    """

    def __init__(self,
                 here: int,
                 there: int):
        assert here is not None
        assert here != 0
        self._here = here
        self._there = there

    @property
    def here(self) -> int:
        return self._here

    @property
    def there(self) -> int:
        return self._there

    def close(self):
        pass

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return "FakeTunnel(here={here},there={there})".format(
            here=self._here,
            there=self._there)

    @property
    def config(self) -> ClusterConfig:
        raise NotImplementedError()
