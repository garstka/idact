"""This module contains the implementation of the cluster interface."""

from typing import Union, Optional, Dict

import bitmath

from idact.core.cluster import Cluster
from idact.core.nodes import Nodes, Node
from idact.core.walltime import Walltime
from idact.detail.allocation.allocation_parameters import AllocationParameters
from idact.detail.config.client. \
    client_cluster_config import ClusterConfigImpl
from idact.detail.nodes.get_access_node import get_access_node
from idact.detail.slurm.allocate_slurm_nodes import allocate_slurm_nodes


class ClusterImpl(Cluster):
    """Implementation of the :class:`.Cluster` interface.

        :param name: Cluster name.

        :param config: Client-side cluster config.

    """

    def __init__(self,
                 name: str,
                 config: ClusterConfigImpl):
        self._name = name
        self._config = config

    def allocate_nodes(self,
                       nodes: int = 1,
                       cores: int = 1,
                       memory_per_node: Union[str, bitmath.Byte] = None,
                       walltime: Union[str, Walltime] = None,
                       native_args: Optional[
                           Dict[str, Optional[
                               str]]] = None) -> Nodes:  # noqa, pylint: disable=bad-whitespace,line-too-long
        if memory_per_node is None:
            memory_per_node = bitmath.GiB(1)
        elif isinstance(memory_per_node, str):
            memory_per_node = bitmath.parse_string(memory_per_node)

        if walltime is None:
            walltime = Walltime(minutes=10)
        elif isinstance(walltime, str):
            walltime = Walltime.from_string(walltime)

        parameters = AllocationParameters(nodes=nodes,
                                          cores=cores,
                                          memory_per_node=memory_per_node,
                                          walltime=walltime,
                                          native_args=native_args)

        return allocate_slurm_nodes(parameters=parameters,
                                    config=self._config)

    def get_access_node(self) -> Node:
        return get_access_node(config=self._config)

    @property
    def name(self) -> str:
        return self._name

    @property
    def config(self) -> ClusterConfigImpl:
        return self._config

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return "Cluster{}".format(self._config)

    def __repr__(self):
        return str(self)
