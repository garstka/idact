from typing import Optional, List

from idact.detail.serialization.serializable import Serializable
from idact.detail.serialization.serializable_types import SerializableTypes


class AppAllocationParameters(Serializable):
    """Allocation parameters from command line.

        :param nodes: Node count.

        :param cores: Core count.

        :param memory_per_node: Memory per node as string.

        :param walltime: Walltime as string.

        :param native_args: Two-element list containing two lists: keys
                            and values for native args.

    """

    def __init__(self,
                 nodes: Optional[int] = None,
                 cores: Optional[int] = None,
                 memory_per_node: Optional[str] = None,
                 walltime: Optional[str] = None,
                 native_args: List[List[str]] = None):
        if nodes is None:
            nodes = 1

        if cores is None:
            cores = 1

        if memory_per_node is None:
            memory_per_node = '1GiB'

        if walltime is None:
            walltime = '0:10:00'

        if native_args is None:
            native_args = [[], []]

        self._nodes = None
        self._cores = None
        self._memory_per_node = None
        self._walltime = None
        self._native_args = None

        self.nodes = nodes
        self.cores = cores
        self.memory_per_node = memory_per_node
        self.walltime = walltime
        self.native_args = native_args

    @property
    def nodes(self) -> int:
        return self._nodes

    @nodes.setter
    def nodes(self, value: int):
        self._nodes = int(value)

    @property
    def cores(self) -> int:
        return self._cores

    @cores.setter
    def cores(self, value: int):
        self._cores = int(value)

    @property
    def memory_per_node(self) -> str:
        return self._memory_per_node

    @memory_per_node.setter
    def memory_per_node(self, value: str):
        self._memory_per_node = str(value)

    @property
    def walltime(self) -> str:
        return self._walltime

    @walltime.setter
    def walltime(self, value: str):
        self._walltime = str(value)

    @property
    def native_args(self) -> List[List[str]]:
        return self._native_args

    @native_args.setter
    def native_args(self, value: List[List[str]]):
        self._native_args = [[str(i) for i in value[0]],
                             [str(i) for i in value[1]]]

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def serialize(self) -> dict:
        return {'type': str(SerializableTypes.APP_ALLOCATION_PARAMETERS),
                'nodes': self._nodes,
                'cores': self._cores,
                'memory_per_node': self._memory_per_node,
                'walltime': self._walltime,
                'native_args': self._native_args}

    @staticmethod
    def deserialize(serialized: dict) -> 'AppAllocationParameters':
        serialized_type = serialized.get(
            'type', str(SerializableTypes.APP_ALLOCATION_PARAMETERS))
        assert serialized_type == str(
            SerializableTypes.APP_ALLOCATION_PARAMETERS)
        return AppAllocationParameters(
            nodes=serialized.get('nodes', None),
            cores=serialized.get('cores', None),
            memory_per_node=serialized.get('memory_per_node', None),
            walltime=serialized.get('walltime', None),
            native_args=serialized.get('native_args', None))
