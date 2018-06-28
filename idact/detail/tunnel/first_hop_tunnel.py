from sshtunnel import SSHTunnelForwarder

from idact.core.tunnel import Tunnel


class FirstHopTunnel(Tunnel):
    """Direct tunnel to the gateway, or any node accessible from localhost.
       Uses pure Python tunneling with sshtunnel.

        :param forwarder: sshtunnel forwarder.

        :param there: remote binding port.
    """

    def __init__(self, forwarder: SSHTunnelForwarder, there: int):
        self._forwarder = forwarder
        self._there = there

        self._forwarder.start()
        self._here = forwarder.local_bind_address[1]

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
        return self._forwarder

    def __str__(self):
        return "{class_name}({here}:{there})".format(
            class_name=self.__class__.__name__,
            here=self.here,
            there=self.there)

    def __repr__(self):
        return str(self)
