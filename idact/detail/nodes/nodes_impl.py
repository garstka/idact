from typing import List, Optional

from idact.core.nodes import Nodes, Node
from idact.detail.allocation.allocation import Allocation
from idact.detail.nodes.node_impl import NodeImpl


class NodesImpl(Nodes):  # pylint: disable=too-many-ancestors
    """Implementation of a collection of nodes.

        :param nodes: Nodes to be part of the collection.

        :param allocation: Allocation request for the nodes.

    """

    def __init__(self,
                 nodes: List[NodeImpl],
                 allocation: Allocation):
        self._nodes = nodes
        self._allocation = allocation

    def wait(self,
             timeout: Optional[float] = None):
        self._allocation.wait(timeout=timeout)

    def cancel(self):
        return self._allocation.cancel()

    def running(self) -> bool:
        return self._allocation.running()

    def __len__(self) -> int:
        return len(self._nodes)

    def __getitem__(self, i: int) -> Node:
        return self._nodes[i]

    def __contains__(self, x: object) -> bool:
        return x in self._nodes

    def __str__(self):
        return "Nodes([{}])".format(','.join(
            [str(node) for node in self._nodes]))

    def __repr__(self):
        return str(self)
