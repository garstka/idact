"""This module contains the internal allocation interface."""

from abc import abstractmethod

from typing import Optional

from idact.detail.serialization.serializable import Serializable


class Allocation(Serializable):
    """Corresponds to a resource allocation request.

        E.g. a Slurm job.
    """

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
        """Returns True, if the job is still running.

           For more, see :meth:`.Nodes.running`.
        """
        pass

    @property
    @abstractmethod
    def waited(self) -> bool:
        """Returns True if successfully waited for allocation."""
        pass
