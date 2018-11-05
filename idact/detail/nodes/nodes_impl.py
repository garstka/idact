"""This module contains the implementation of the interface for a collection
    of nodes."""
from typing import List, Optional

from idact.core.config import ClusterConfig
from idact.core.nodes import Nodes, Node
from idact.detail.allocation.allocation import Allocation
from idact.detail.helper.get_uuid import get_uuid
from idact.detail.nodes.node_internal import NodeInternal
from idact.detail.serialization.serializable import Serializable
from idact.detail.nodes.node_impl import NodeImpl
from idact.detail.serialization.serializable_types import SerializableTypes
from idact.detail.slurm.slurm_allocation import SlurmAllocation


class NodesImpl(Nodes, Serializable):  # pylint: disable=too-many-ancestors
    """Implementation of a collection of nodes.

        :param nodes: Nodes to be part of the collection.

        :param allocation: Allocation request for the nodes.

        :param uuid: Unique deployment identifier.

    """

    def __init__(self,
                 nodes: List[NodeImpl],
                 allocation: Allocation,
                 uuid: Optional[str] = None):
        self._nodes = nodes
        self._allocation = allocation
        self._uuid = uuid if uuid is not None else get_uuid()

    @property
    def uuid(self) -> str:
        """Unique deployment id."""
        return self._uuid

    def wait(self,
             timeout: Optional[float] = None):
        self._allocation.wait(timeout=timeout)

    def cancel(self):
        return self._allocation.cancel()

    def running(self) -> bool:
        return self._allocation.running()

    @property
    def waited(self) -> bool:
        return self._allocation.waited

    def __len__(self) -> int:
        return len(self._nodes)

    def __getitem__(self, i: int) -> Node:
        return self._nodes[i]

    def __contains__(self, x: object) -> bool:
        return x in self._nodes

    def __str__(self):
        return "Nodes([{nodes}], {allocation})".format(
            nodes=','.join([str(node) for node in self._nodes]),
            allocation=self._allocation)

    def __repr__(self):
        return str(self)

    def serialize(self) -> dict:
        return {'type': str(SerializableTypes.NODES_IMPL),
                'nodes': [node.serialize() for node in self._nodes],
                'allocation': self._allocation.serialize()}

    @staticmethod
    def deserialize(config: ClusterConfig,
                    access_node: NodeInternal,
                    uuid: str,
                    serialized: dict) -> 'NodesImpl':
        try:
            assert serialized['type'] == str(SerializableTypes.NODES_IMPL)
            nodes = [NodeImpl.deserialize(config=config, serialized=node)
                     for node in serialized['nodes']]
            allocation = SlurmAllocation.deserialize(
                access_node=access_node,
                nodes=nodes,
                serialized=serialized['allocation'])
            return NodesImpl(nodes=nodes,
                             allocation=allocation,
                             uuid=uuid)
        except KeyError as e:
            raise RuntimeError("Unable to deserialize.") from e

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
