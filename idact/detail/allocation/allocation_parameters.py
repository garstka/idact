from typing import Optional, Any, Dict

import bitmath

from idact.core.walltime import Walltime


class AllocationParameters:
    """Union of all cluster job allocation parameters, regardless of
       the workflow manager.

       For detailed parameter descriptions, see
       :meth:`.Cluster.allocate_nodes`.
    """

    def __init__(self,
                 nodes: Optional[int] = None,
                 cores: Optional[int] = None,
                 memory_per_node: Optional[bitmath.Byte] = None,
                 walltime: Optional[Walltime] = None,
                 native_args: Optional[Dict[str, Optional[str]]] = None):
        self._nodes = nodes
        self._cores = cores
        self._memory_per_node = memory_per_node
        self._walltime = walltime

        self._all = {'nodes': self._nodes,
                     'cores': self._cores,
                     'memory_per_node': self._memory_per_node,
                     'walltime': self._walltime}

        self._native_args = native_args if native_args else {}

    @property
    def nodes(self) -> Optional[int]:
        return self._nodes

    @property
    def cores(self) -> Optional[int]:
        return self._cores

    @property
    def memory_per_node(self) -> Optional[bitmath.Byte]:
        return self._memory_per_node

    @property
    def walltime(self) -> Optional[Walltime]:
        return self._walltime

    @property
    def all(self) -> Dict[str, Any]:
        return self._all

    @property
    def native_args(self) -> Dict[str, Optional[str]]:
        return self._native_args
