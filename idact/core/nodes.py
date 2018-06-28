"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.Node`, :class:`.Nodes`.
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from typing import Optional

from idact.core.tunnel import Tunnel


class Node(ABC):
    """Cluster node interface."""

    @abstractmethod
    def run(self, command: str, timeout: Optional[int] = None) -> str:
        """Runs a command on the node. Returns the result as string.

            :param command: Command to run.

            :param timeout: Execution timeout.
        """
        pass

    @abstractmethod
    def tunnel(self,
               there: int,
               here: Optional[int] = None) -> Tunnel:
        """Creates an SSH tunnel from node to localhost.

            :param there: Remote port to tunnel.

            :param here: Local port, or None for any port.
        """
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
