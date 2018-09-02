"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.NodeResourceStatus`.
"""

from abc import ABC, abstractmethod
from typing import Optional

import bitmath


class NodeResourceStatus(ABC):
    """Cluster node resource status interface."""

    @property
    @abstractmethod
    def memory_total(self) -> Optional[bitmath.GiB]:
        """Total allocated memory limit.
            Returns None for a node that was not allocated by a workload
            manager."""
        pass

    @property
    @abstractmethod
    def memory_usage(self) -> bitmath.GiB:
        """Sum of RES (Resident Memory Size) of all user processes on the node
            as reported by top.
            Can be greater than memory_total, if multiple allocations
            of the same user are running on the node."""
        pass

    @property
    @abstractmethod
    def cpu_cores(self) -> int:
        """Allocated core count.
            Returns None for a node that was not allocated by a workload
            manager."""
        pass

    @property
    @abstractmethod
    def cpu_usage(self) -> float:
        """Sum of %CPU of all user processes as reported by top.
            Can be greater than 100.0, if multiple cores are used, or multiple
            allocations of the same user are running on the node.
        """
        pass
