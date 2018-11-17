"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.JupyterDeployment`.
"""
from abc import ABC, abstractmethod


class JupyterDeployment(ABC):
    """Jupyter notebook deployment on a node."""

    @property
    @abstractmethod
    def local_port(self) -> int:
        """The local access port."""
        pass

    @property
    @abstractmethod
    def address(self) -> str:
        """Local notebook address."""
        pass

    @abstractmethod
    def open_in_browser(self):
        """Opens the notebook server in the local browser."""
        pass

    @abstractmethod
    def cancel(self):
        """Closes the notebook server and the tunnel."""
        pass

    @abstractmethod
    def cancel_local(self):
        """Closes the tunnel, but does not cancel the deployment."""
        pass
