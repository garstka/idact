from idact.core.config import ClusterConfig
from idact.core.synchronized_deployments import SynchronizedDeployments
from idact.detail.deployment_sync.deployment_definitions import \
    DeploymentDefinitions
from idact.detail.deployment_sync.nodes.materialize_nodes import \
    materialize_nodes
from idact.detail.deployment_sync.synchronized_deployments_impl import \
    SynchronizedDeploymentsImpl
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_internal import NodeInternal


# pylint: disable=bad-continuation
def materialize_deployments(
    config: ClusterConfig,
    access_node: NodeInternal,
    deployments: DeploymentDefinitions) -> SynchronizedDeployments:  # noqa
    """Creates deployment objects from definitions.

        :param config: Cluster config.

        :param access_node: Cluster access node.

        :param deployments: Definitions to materialize.

    """

    all_nodes_with_expiration_dates = []
    for uuid, definition in deployments.nodes.items():
        materialized_nodes = materialize_nodes(config=config,
                                               access_node=access_node,
                                               uuid=uuid,
                                               definition=definition)
        all_nodes_with_expiration_dates.append(
            (materialized_nodes, definition.expiration_date))

    sorted_nodes = [nodes for (nodes, expiration_date)
                    in sorted(all_nodes_with_expiration_dates,
                              key=lambda value: value[1])]

    log = get_logger(__name__)
    for node in sorted_nodes:
        log.info("Pulled node deployment: %s", node)
    return SynchronizedDeploymentsImpl(nodes=sorted_nodes)
