"""This module contains the implementation of an SSH tunnel binding parameter.
"""

from typing import Tuple


class Binding:
    """Ssh tunnel binding.

        :param address: IPv4 address or hostname. Can be empty for local
                        binding.

        :param port:    Port number. Zero for a local binding means any
                        free port.

    """

    def __init__(self, address: str, port: int):
        self._address = address
        self._port = port

    @property
    def address(self) -> str:
        """IPv4 address or hostname."""
        return self._address

    @property
    def port(self) -> int:
        """Port number."""
        return self._port

    def as_tuple(self) -> Tuple[str, int]:
        """Returns the tuple (address, port)."""
        return self.address, self.port
