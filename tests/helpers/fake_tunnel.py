from contextlib import contextmanager

from idact import ClusterConfig
from idact.detail.nodes.node_impl import NodeImpl
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

    def __repr__(self):
        return str(self)

    @property
    def config(self) -> ClusterConfig:
        raise NotImplementedError()


@contextmanager
def use_fake_tunnel():
    """A context manager that replaces :meth:`.NodeImpl.tunnel` with
        a method returning :class:`.FakeTunnel`."""

    def fake_tunnel(_, there: int, here: int):
        return FakeTunnel(here=here, there=there)

    saved_tunnel = NodeImpl.tunnel
    try:
        NodeImpl.tunnel = fake_tunnel
        yield
    finally:
        NodeImpl.tunnel = saved_tunnel
