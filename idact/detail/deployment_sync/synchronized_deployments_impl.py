from typing import List

from idact.core.dask_deployment import DaskDeployment
from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.nodes import Nodes
from idact.core.synchronized_deployments import SynchronizedDeployments


class SynchronizedDeploymentsImpl(SynchronizedDeployments):
    """Deployments synchronized from the cluster.

        :param nodes: Synchronized allocations.
        :param jupyter_deployments: Synchronized Jupyter deployments.
        :param dask_deployments: Synchronized Dask deployments.

    """

    def __init__(self,
                 nodes: List[Nodes] = None,
                 jupyter_deployments: List[JupyterDeployment] = None,
                 dask_deployments: List[DaskDeployment] = None):
        self._nodes = nodes if nodes is not None else []
        self._jupyter_deployments = (
            jupyter_deployments
            if jupyter_deployments is not None else [])
        self._dask_deployments = (dask_deployments
                                  if dask_deployments is not None else [])

    @property
    def nodes(self) -> List[Nodes]:
        return self._nodes

    @property
    def jupyter_deployments(self) -> List[JupyterDeployment]:
        return self._jupyter_deployments

    @property
    def dask_deployments(self) -> List[DaskDeployment]:
        return self._dask_deployments

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        to_format = ("SynchronizedDeployments(nodes={nodes},"
                     " jupyter_deployments={jupyter_deployments},"
                     " dask_deployments={dask_deployments})")
        return to_format.format(nodes=len(self._nodes),
                                jupyter_deployments=len(
                                    self._jupyter_deployments),
                                dask_deployments=len(
                                    self._dask_deployments))

    def __repr__(self):
        return str(self)
