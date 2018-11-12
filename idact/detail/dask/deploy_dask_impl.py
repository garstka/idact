from contextlib import ExitStack
from typing import Sequence, List, Tuple

from idact.core.config import ClusterConfig
from idact.core.nodes import Node
from idact.core.retry import Retry
from idact.detail.dask.check_scheduler_reachable import \
    check_scheduler_reachable
from idact.detail.dask.dask_scheduler_deployment import DaskSchedulerDeployment
from idact.detail.dask.dask_worker_deployment import DaskWorkerDeployment
from idact.detail.dask.deploy_dask_scheduler import deploy_dask_scheduler
from idact.detail.dask.deploy_dask_worker import deploy_dask_worker
from idact.detail.dask.validate_worker import validate_worker
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.deployment.cancel_on_failure import cancel_on_failure
from idact.detail.helper.retry import retry_with_config
from idact.detail.helper.stage_info import stage_info
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_internal import NodeInternal


def connect_to_each_node(nodes: Sequence[Node],
                         config: ClusterConfig):
    """Connects to each node to make sure any connection issues come up
        before attempting to actually deploy anything.

         :param nodes: Nodes to deploy Dask on.

         :param config: Cluster config.

    """
    log = get_logger(__name__)
    node_count = len(nodes)
    for i, node in enumerate(nodes):
        with stage_info(log,
                        "Connecting to %s:%d (%d/%d).",
                        node.host, node.port,
                        i + 1, node_count):
            retry_with_config(node.connect,
                              name=Retry.DASK_NODE_CONNECT,
                              config=config)


def check_scheduler_reachable_from_nodes(nodes: Sequence[Node],
                                         scheduler: DaskSchedulerDeployment,
                                         config: ClusterConfig):
    """Checks whether connection to the scheduler is possible from each node,
        before deploying workers.

         :param nodes: Nodes to deploy Dask on.

         :param scheduler: Scheduler to connect to.

         :param config: Cluster config.

    """
    log = get_logger(__name__)
    node_count = len(nodes)
    for i, node in enumerate(nodes):
        with stage_info(log,
                        "Checking scheduler connectivity from %s (%d/%d).",
                        node.host,
                        i + 1, node_count):
            retry_with_config(lambda n=node:
                              check_scheduler_reachable(node=n,
                                                        scheduler=scheduler),
                              name=Retry.SCHEDULER_CONNECT,
                              config=config)


# pylint: disable=bad-continuation,bad-whitespace
def deploy_scheduler_on_first_node(
    nodes: Sequence[Node]) -> DaskSchedulerDeployment:  # noqa
    """Deploys a scheduler on the first node in the node sequence.

        :param nodes: Nodes to deploy Dask on.

    """
    log = get_logger(__name__)
    assert isinstance(nodes[0], NodeInternal)
    first_node = nodes[0]  # type: NodeInternal

    with stage_info(log, "Deploying scheduler on the first node: %s.",
                    first_node.host):
        scheduler = retry_with_config(
            lambda: deploy_dask_scheduler(node=first_node),
            name=Retry.DEPLOY_DASK_SCHEDULER,
            config=first_node.config)
        return scheduler


def deploy_worker_on_node(node: Node,
                          scheduler: DaskSchedulerDeployment,
                          worker_number: int,
                          worker_count: int) -> DaskWorkerDeployment:
    """Deploys a worker on the node. Retries on failure.

        :param node: Node to deploy a worker on.

        :param scheduler: Scheduler for the worker.

        :param worker_number: Worker number out of workers to deploy.

        :param worker_count: Count of workers being deployed

    """
    log = get_logger(__name__)
    with stage_info(log, "Deploying worker %d/%d.",
                    worker_number, worker_count):
        assert isinstance(node, NodeInternal)
        node_impl = node  # type: NodeInternal
        worker = retry_with_config(
            lambda: deploy_dask_worker(node=node_impl,
                                       scheduler=scheduler),
            name=Retry.DEPLOY_DASK_WORKER,
            config=node_impl.config)
        return worker


def deploy_workers_on_each_node(nodes: Sequence[Node],
                                scheduler: DaskSchedulerDeployment,
                                stack: ExitStack) \
    -> List[
        DaskWorkerDeployment]:
    """Deploys workers on each node.

        :param nodes: Nodes to deploy workers on.

        :param scheduler: Scheduler for workers.

        :param stack: Exit stack. Workers will be cancelled on failure.

    """
    log = get_logger(__name__)
    workers = []
    with stage_info(log, "Deploying workers."):
        total = len(nodes)
        for i, node in enumerate(nodes):
            worker = deploy_worker_on_node(node=node,
                                           scheduler=scheduler,
                                           worker_number=i + 1,
                                           worker_count=total)
            stack.enter_context(cancel_on_failure(worker))
            workers.append(worker)
    return workers


def discard_invalid_workers(workers: List[DaskWorkerDeployment],
                            stack: ExitStack) \
    -> Tuple[
        List[DaskWorkerDeployment],
        List[Node]]:
    """Validates each worker. Returns a tuple of valid workers and nodes
        for which the workers could not be validated.

        :param workers: Workers to validate.

        :param stack: Exit stack. Failed workers will be cancelled on exit.

    """
    log = get_logger(__name__)
    valid_workers = []
    nodes_to_redeploy = []
    worker_count = len(workers)
    for i, worker in enumerate(workers):
        try:
            with stage_info(log, "Validating worker %d/%d.",
                            i + 1, worker_count):
                validate_worker(worker=worker)
            valid_workers.append(worker)
        except Exception:  # noqa, pylint: disable=broad-except
            log.debug("Failed to validate worker. Exception:", exc_info=1)
            nodes_to_redeploy.append(worker.deployment.node)
            stack.enter_context(cancel_on_exit(worker))

    return valid_workers, nodes_to_redeploy
