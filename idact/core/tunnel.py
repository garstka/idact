"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.Tunnel`.
"""
from abc import abstractmethod, ABC


class Tunnel(ABC):
    """SSH tunnel."""

    @property
    @abstractmethod
    def there(self) -> int:
        """The remote port."""
        pass

    @property
    @abstractmethod
    def here(self) -> int:
        """The local port."""
        pass

    @abstractmethod
    def close(self):
        """Closes the tunnel."""
        pass
