from idact import Tunnel


class FakeTunnelAnyLocalPort(Tunnel):
    """Does nothing besides holding the remote port.
        Local port is ignored.

        :param there: Remote port.

    """

    def __init__(self, there: int):
        self._there = there

    @property
    def there(self) -> int:
        return self._there

    @property
    def here(self) -> int:
        return 0

    def close(self):
        pass

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return "FakeTunnelAnyLocalPort(there={there})".format(
            there=self._there)
