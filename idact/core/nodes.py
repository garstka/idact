from abc import ABC, abstractmethod
from collections.abc import Sequence

from typing import Optional


class Node(ABC):
    """Cluster node interface."""

    @abstractmethod
    def run(self, command: str) -> str:
        """Runs a command on the node. Returns the result as string."""
        pass


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
        """Returns true if the nodes are running."""
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
