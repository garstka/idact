from abc import ABC, abstractmethod

from typing import List

import dask.distributed


class DaskDiagnostics(ABC):
    """Bokeh diagnostics for a deployment of Dask."""

    @property
    @abstractmethod
    def addresses(self) -> List[str]:
        """Returns local addresses of the tunnelled diagnostics servers."""
        pass

    @abstractmethod
    def open_all(self):
        """Opens all diagnostics servers in a web browser (in separate tabs).
        """
        pass


class DaskDeployment(ABC):
    """Deployment of Dask on a cluster."""

    @abstractmethod
    def get_client(self) -> dask.distributed.Client:
        """Returns a Dask client set up to work with this deployment."""
        pass

    @property
    @abstractmethod
    def diagnostics(self) -> DaskDiagnostics:
        """Dask diagnostics server tunnels."""
        pass

    @abstractmethod
    def cancel(self):
        """Cancels the deployment."""
        pass
