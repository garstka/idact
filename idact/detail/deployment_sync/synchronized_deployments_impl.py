from typing import List

from idact.core.nodes import Nodes
from idact.core.synchronized_deployments import SynchronizedDeployments


class SynchronizedDeploymentsImpl(SynchronizedDeployments):
    """Deployments synchronized from the cluster.

        :param nodes: Synchronized allocations.
    """

    def __init__(self, nodes: List[Nodes]):
        self._nodes = nodes

    @property
    def nodes(self) -> List[Nodes]:
        return self._nodes

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return "SynchronizedDeployments(nodes={})".format(len(self._nodes))

    def __repr__(self):
        return str(self)
