"""Contents of this module are intended to be imported into
   the top-level package.

   See :func:`.deploy_dask`.
"""

from contextlib import ExitStack
from typing import Sequence

from idact.core.dask_deployment import DaskDeployment
from idact.detail.dask.dask_deployment_impl import DaskDeploymentImpl
from idact.detail.dask.deploy_dask_scheduler import deploy_dask_scheduler
from idact.detail.dask.deploy_dask_worker import deploy_dask_worker
from idact.detail.deployment.cancel_on_failure import cancel_on_failure
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_internal import NodeInternal


def deploy_dask(nodes: Sequence) -> DaskDeployment:
    """Deploys Dask on cluster nodes.

        Dask scheduler will be deployed on the first node.
        Dask workers will be deployed on each node.

        :param nodes: Nodes for Dask to be deployed on.

    """
    if not nodes:
        raise ValueError("At least one node is required for Dask deployment.")

    log = get_logger(__name__)
    first_node = nodes[0]
    assert isinstance(first_node, NodeInternal)
    log.info("Deploying scheduler...")
    scheduler = deploy_dask_scheduler(node=first_node)
    workers = []
    log.info("Deploying workers...")
    with ExitStack() as stack:
        stack.enter_context(cancel_on_failure(scheduler))
        total = len(nodes)
        for i, node in enumerate(nodes):
            log.info("Deploying worker %d/%d...", i + 1, total)
            assert isinstance(node, NodeInternal)
            worker = deploy_dask_worker(node=node,
                                        scheduler=scheduler)
            stack.enter_context(cancel_on_failure(worker))
            workers.append(worker)

        return DaskDeploymentImpl(scheduler=scheduler,
                                  workers=workers)
