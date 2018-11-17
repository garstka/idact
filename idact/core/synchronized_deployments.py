"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.SynchronizedDeployments`.
"""

from abc import ABC, abstractmethod
from typing import List

from idact.core.dask_deployment import DaskDeployment
from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.nodes import Nodes


class SynchronizedDeployments(ABC):
    """Deployments synchronized from the cluster."""

    @property
    @abstractmethod
    def nodes(self) -> List[Nodes]:
        """Synchronized allocations."""
        pass

    @property
    @abstractmethod
    def jupyter_deployments(self) -> List[JupyterDeployment]:
        """Synchronized Jupyter deployments."""
        pass

    @property
    @abstractmethod
    def dask_deployments(self) -> List[DaskDeployment]:
        """Synchronized Dask deployments."""
        pass
