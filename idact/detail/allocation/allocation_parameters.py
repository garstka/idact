"""This module contains generic allocation parameters."""

from typing import Optional, Any, Dict

import bitmath

from idact.core.walltime import Walltime
from idact.detail.serialization.serializable import Serializable
from idact.detail.serialization.serializable_types import SerializableTypes


class AllocationParameters(Serializable):
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
        """Cluster node count."""
        return self._nodes

    @property
    def cores(self) -> Optional[int]:
        """CPU core count per node."""
        return self._cores

    @property
    def memory_per_node(self) -> Optional[bitmath.Byte]:
        """Memory per node."""
        return self._memory_per_node

    @property
    def walltime(self) -> Optional[Walltime]:
        """Maximum time to allocate the resources for."""
        return self._walltime

    @property
    def all(self) -> Dict[str, Any]:
        """All parameters by name."""
        return self._all

    @property
    def native_args(self) -> Dict[str, Optional[str]]:
        """Native arguments for the workload manager."""
        return self._native_args

    def serialize(self) -> dict:
        return {'type': str(SerializableTypes.ALLOCATION_PARAMETERS),
                'nodes': self._nodes,
                'cores': self._cores,
                'memory_per_node': (None if self._memory_per_node is None
                                    else str(self._memory_per_node)),
                'walltime': (None if self._walltime is None
                             else str(self._walltime)),
                'native_args': self._native_args}

    @staticmethod
    def deserialize(serialized: dict) -> 'AllocationParameters':
        try:
            assert serialized['type'] == str(
                SerializableTypes.ALLOCATION_PARAMETERS)
            return AllocationParameters(
                nodes=serialized['nodes'],
                cores=serialized['cores'],
                memory_per_node=(
                    None if serialized['memory_per_node'] is None
                    else bitmath.parse_string(serialized['memory_per_node'])),
                walltime=(None if serialized['walltime'] is None
                          else Walltime.from_string(serialized['walltime'])),
                native_args=serialized['native_args'])
        except KeyError as e:
            raise RuntimeError("Unable to deserialize.") from e

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
