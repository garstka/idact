import datetime
from typing import Tuple, Any, List

from idact.core.config import ClusterConfig
from idact.core.synchronized_deployments import SynchronizedDeployments
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


# pylint: disable=bad-continuation
def sort_deployments_by_expiration_dates(
    nodes: List[Tuple[Any, datetime.datetime]],
    jupyter_deployments: List[Tuple[Any, datetime.datetime]]) \
    -> Tuple[List[Any], List[Any]]:  # noqa
    """Sorts each group of deployments by expiration dates.
        Discards the expiration dates.

        :param nodes: Allocation deployments.

        :param jupyter_deployments: Jupyter deployments.

    """
    return (sorted_by_expiration_date(nodes),
            sorted_by_expiration_date(jupyter_deployments))


def report_pulled_deployments(deployments: SynchronizedDeploymentsImpl):
    """Prints pulled deployments.

        :param deployments: Deployments to report.

    """
    log = get_logger(__name__)
    for node in deployments.nodes:
        log.info("Pulled allocation deployment: %s", node)
    for jupyter in deployments.jupyter_deployments:
        log.info("Pulled Jupyter deployment: %s", jupyter)


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

    nodes_by_date = []
    for uuid, definition in deployments.nodes.items():
        materialized_nodes = materialize_nodes(config=config,
                                               access_node=access_node,
                                               uuid=uuid,
                                               definition=definition)
        nodes_by_date.append(
            (materialized_nodes, definition.expiration_date))

    jupyter_deployments_by_date = []
    for uuid, definition in deployments.jupyter_deployments.items():
        materialized_jupyter = materialize_jupyter_deployment(
            config=config,
            uuid=uuid,
            definition=definition)
        jupyter_deployments_by_date.append(
            (materialized_jupyter, definition.expiration_date))

    nodes, jupyter_deployments = sort_deployments_by_expiration_dates(
        nodes=nodes_by_date,
        jupyter_deployments=jupyter_deployments_by_date)

    synchronized_deployments = SynchronizedDeploymentsImpl(
        nodes=nodes,
        jupyter_deployments=jupyter_deployments)

    report_pulled_deployments(deployments=synchronized_deployments)

    return synchronized_deployments
