from typing import Optional

import bitmath

from idact.core.node_resource_status import NodeResourceStatus
from idact.detail.nodes.get_node_cpu_usage import get_node_cpu_usage
from idact.detail.nodes.get_node_memory_usage import get_node_memory_usage
from idact.detail.nodes.node_internal import NodeInternal


class NodeResourceStatusImpl(NodeResourceStatus):
    """Implementation of the cluster node resource status interface."""

    def __init__(self, node: NodeInternal):
        self._node = node

    @property
    def memory_total(self) -> Optional[bitmath.GiB]:
        memory = self._node.memory
        if memory is None:
            return memory
        return memory.to_GiB()

    @property
    def memory_usage(self) -> bitmath.GiB:
        memory = get_node_memory_usage(node=self._node)
        return memory.to_GiB()

    @property
    def cpu_cores(self) -> int:
        return self._node.cores

    @property
    def cpu_usage(self) -> float:
        return get_node_cpu_usage(node=self._node)
