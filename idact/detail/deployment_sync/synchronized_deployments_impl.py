from typing import List

from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.nodes import Nodes
from idact.core.synchronized_deployments import SynchronizedDeployments


class SynchronizedDeploymentsImpl(SynchronizedDeployments):
    """Deployments synchronized from the cluster.

        :param nodes: Synchronized allocations.
        :param jupyter_deployments: Synchronized Jupyter deployments.

    """

    def __init__(self,
                 nodes: List[Nodes] = None,
                 jupyter_deployments: List[JupyterDeployment] = None):
        self._nodes = nodes if nodes is not None else []
        self._jupyter_deployment = (jupyter_deployments
                                    if jupyter_deployments is not None else [])

    @property
    def nodes(self) -> List[Nodes]:
        return self._nodes

    @property
    def jupyter_deployments(self) -> List[JupyterDeployment]:
        return self._jupyter_deployment

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        to_format = ("SynchronizedDeployments(nodes={nodes},"
                     " jupyter_deployments={jupyter_deployments})")
        return to_format.format(nodes=len(self._nodes),
                                jupyter_deployments=len(
                                    self._jupyter_deployment))

    def __repr__(self):
        return str(self)
