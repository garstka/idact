from abc import ABC, abstractmethod
from typing import List

from idact.core.nodes import Nodes


class SynchronizedDeployments(ABC):
    """Deployments synchronized from the cluster."""

    @property
    @abstractmethod
    def nodes(self) -> List[Nodes]:
        """Synchronized allocations."""
        pass
