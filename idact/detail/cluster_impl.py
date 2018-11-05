"""This module contains the implementation of the cluster interface."""

from typing import Union, Optional, Dict

import bitmath

from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.dask_deployment import DaskDeployment
from idact.core.config import ClusterConfig
from idact.core.cluster import Cluster
from idact.core.nodes import Nodes
from idact.core.synchronized_deployments import SynchronizedDeployments
from idact.core.walltime import Walltime
from idact.detail.allocation.allocation_parameters import AllocationParameters
from idact.detail.deployment_sync.add_deployment_definition import \
    add_deployment_definition
from idact.detail.deployment_sync.deployment_definitions import \
    DeploymentDefinitions
from idact.detail.deployment_sync.deployment_definitions_serialization import \
    deserialize_deployment_definitions_from_cluster, \
    deployment_definitions_file_exists, \
    serialize_deployment_definitions_to_cluster, \
    remove_serialized_deployment_definitions
from idact.detail.deployment_sync.discard_expired_deployments import \
    discard_expired_deployments
from idact.detail.deployment_sync.discard_non_functional_deployments import \
    discard_non_functional_deployments
from idact.detail.deployment_sync.install_compute_node_access_key import \
    install_compute_node_access_key
from idact.detail.deployment_sync.materialize_deployments import \
    materialize_deployments
from idact.detail.deployment_sync.synchronized_deployments_impl import \
    SynchronizedDeploymentsImpl
from idact.detail.helper.stage_info import stage_info
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.get_access_node import get_access_node
from idact.detail.nodes.node_internal import NodeInternal
from idact.detail.slurm.allocate_slurm_nodes import allocate_slurm_nodes


class ClusterImpl(Cluster):
    """Implementation of the :class:`.Cluster` interface.

        :param name: Cluster name.

        :param config: Client-side cluster config.

    """

    def __init__(self,
                 name: str,
                 config: ClusterConfig):
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

    def get_access_node(self) -> NodeInternal:
        return get_access_node(config=self._config)

    @property
    def name(self) -> str:
        return self._name

    @property
    def config(self) -> ClusterConfig:
        return self._config

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return "Cluster{}".format(self._config)

    def __repr__(self):
        return str(self)

    def push_deployment(self, deployment: Union[Nodes,
                                                JupyterDeployment,
                                                DaskDeployment]):
        log = get_logger(__name__)
        with stage_info(log, "Pushing deployment: %s", deployment):
            log = get_logger(__name__)
            node = self.get_access_node()
            if deployment_definitions_file_exists(node=node):
                deployments = deserialize_deployment_definitions_from_cluster(
                    node=node)
            else:
                log.debug(
                    "No deployment definitions file, defaulting to empty.")
                deployments = DeploymentDefinitions()

            deployments = discard_expired_deployments(deployments)

            add_deployment_definition(deployments=deployments,
                                      deployment=deployment)

            serialize_deployment_definitions_to_cluster(
                node=node,
                deployments=deployments)

    def pull_deployments(self) -> SynchronizedDeployments:
        log = get_logger(__name__)
        with stage_info(log, "Pulling deployments."):
            access_node = self.get_access_node()
            if not deployment_definitions_file_exists(node=access_node):
                log.info("No deployment definitions were found.")
                return SynchronizedDeploymentsImpl(nodes=[])

            deployments = deserialize_deployment_definitions_from_cluster(
                node=access_node)
            deployments = discard_expired_deployments(deployments)
            install_compute_node_access_key(access_node=access_node)
            materialized_deployments = materialize_deployments(
                config=self._config,
                access_node=access_node,
                deployments=deployments)
            materialized_deployments = discard_non_functional_deployments(
                deployments=materialized_deployments)
            return materialized_deployments

    def clear_pushed_deployments(self):
        log = get_logger(__name__)
        with stage_info(log, "Clearing deployments."):
            node = self.get_access_node()
            remove_serialized_deployment_definitions(node=node)
