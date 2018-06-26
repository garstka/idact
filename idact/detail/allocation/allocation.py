from abc import ABC, abstractmethod

from typing import Optional


class Allocation(ABC):
    """Corresponds to a resource allocation request, e.g. a Slurm job."""

    @abstractmethod
    def wait(self,
             timeout: Optional[float]):
        """Waits for allocation.

           For parameter description, see :meth:`.Nodes.wait`.
        """
        pass

    @abstractmethod
    def cancel(self):
        """Cancels the allocation.

           For more, see :meth:`.Nodes.cancel`."""
        pass

    @abstractmethod
    def running(self) -> bool:
        """Returns true, if the job is still running.

           For more, see :meth:`.Nodes.running`.
        """
        pass
