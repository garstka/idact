"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.Nodes`.
"""

from abc import abstractmethod
from collections.abc import Sequence

from typing import Optional

from idact.core.node import Node


class Nodes(Sequence):
    """Collection of cluster nodes allocated together."""

    @abstractmethod
    def wait(self,
             timeout: Optional[float] = None):
        """Waits until the nodes are allocated.

            :param timeout: Maximum number of seconds to wait for allocation.
                            None is treated as no limit.

            :raises RuntimeException: On error.

            :raises TimeoutException: On timeout.
        """
        pass

    @abstractmethod
    def cancel(self):
        """Deallocates the nodes or cancels the allocation request."""
        pass

    @abstractmethod
    def running(self) -> bool:
        """Returns True if the nodes are running."""
        pass

    @property
    @abstractmethod
    def waited(self) -> bool:
        """Returns True if successfully waited for allocation."""
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __getitem__(self, i: int) -> Node:
        pass

    @abstractmethod
    def __contains__(self, x: object) -> bool:
        pass
