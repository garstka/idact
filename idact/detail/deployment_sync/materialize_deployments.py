import datetime
from typing import Tuple, Any, List

from idact.core.config import ClusterConfig
from idact.core.synchronized_deployments import SynchronizedDeployments
from idact.detail.deployment_sync.dask_deployments. \
    materialize_dask_deployment import materialize_dask_deployment
from idact.detail.deployment_sync.deployment_definitions import \
    DeploymentDefinitions
from idact.detail.deployment_sync.jupyter_deployments. \
    materialize_jupyter_deployment import materialize_jupyter_deployment
from idact.detail.deployment_sync.nodes.materialize_nodes import \
    materialize_nodes
from idact.detail.deployment_sync.synchronized_deployments_impl import \
    SynchronizedDeploymentsImpl
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_internal import NodeInternal


# pylint: disable=bad-continuation
def sorted_by_expiration_date(
    to_sort: List[Tuple[Any, datetime.datetime]]) -> List[Any]:  # noqa
    """Returns the values sorted by expiration date, discarding the date."""
    return [first for (first, expiration_date)
            in sorted(to_sort, key=lambda value: value[1])]


def report_pulled_deployments(deployments: SynchronizedDeploymentsImpl):
    """Prints pulled deployments.

        :param deployments: Deployments to report.

    """
    log = get_logger(__name__)
    for node in deployments.nodes:
        log.info("Pulled allocation deployment: %s", node)
    for jupyter in deployments.jupyter_deployments:
        log.info("Pulled Jupyter deployment: %s", jupyter)
    for dask in deployments.dask_deployments:
        log.info("Pulled Dask deployment: %s", dask)


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
    log = get_logger(__name__)

    nodes_index = 0
    jupyter_index = 1
    dask_index = 2
    deployments_by_date = ([], [], [])

    for uuid, definition in deployments.nodes.items():
        try:
            materialized_nodes = materialize_nodes(config=config,
                                                   access_node=access_node,
                                                   uuid=uuid,
                                                   definition=definition)
            deployments_by_date[nodes_index].append(
                (materialized_nodes, definition.expiration_date))
        except RuntimeError:
            log.warning("Discarding a synchronized allocation deployment,"
                        " unable to materialize: %s", uuid)
            log.debug("Exception", exc_info=1)

    for uuid, definition in deployments.jupyter_deployments.items():
        try:
            materialized_jupyter = materialize_jupyter_deployment(
                config=config,
                uuid=uuid,
                definition=definition)
            deployments_by_date[jupyter_index].append(
                (materialized_jupyter, definition.expiration_date))
        except RuntimeError:
            log.warning("Discarding a Jupyter deployment,"
                        " unable to materialize: %s", uuid)
            log.debug("Exception", exc_info=1)

    for uuid, definition in deployments.dask_deployments.items():
        try:
            materialized_dask = materialize_dask_deployment(
                config=config,
                uuid=uuid,
                definition=definition)
            deployments_by_date[dask_index].append(
                (materialized_dask, definition.expiration_date))
        except RuntimeError:
            log.warning("Discarding a Dask deployment,"
                        " unable to materialize: %s", uuid)
            log.debug("Exception", exc_info=1)

    deployments_sorted = tuple(map(sorted_by_expiration_date,
                                   deployments_by_date))

    synchronized_deployments = SynchronizedDeploymentsImpl(
        nodes=deployments_sorted[nodes_index],
        jupyter_deployments=deployments_sorted[jupyter_index],
        dask_deployments=deployments_sorted[dask_index])

    report_pulled_deployments(deployments=synchronized_deployments)

    return synchronized_deployments
