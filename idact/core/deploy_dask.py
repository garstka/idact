"""Contents of this module are intended to be imported into
   the top-level package.

   See :func:`.deploy_dask`.
"""

from contextlib import ExitStack
from typing import Sequence

from idact.core.nodes import Node
from idact.core.dask_deployment import DaskDeployment
from idact.detail.dask.dask_deployment_impl import DaskDeploymentImpl
from idact.detail.dask.deploy_dask_impl import connect_to_each_node, \
    deploy_scheduler_on_first_node, deploy_workers_on_each_node, \
    discard_invalid_workers, check_scheduler_reachable_from_nodes
from idact.detail.deployment.cancel_on_failure import cancel_on_failure
from idact.detail.helper.stage_info import stage_info
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_internal import NodeInternal


def deploy_dask(nodes: Sequence[Node]) -> DaskDeployment:
    """Deploys Dask on cluster nodes.

        Dask scheduler will be deployed on the first node.
        Dask workers will be deployed on each node.

        :param nodes: Nodes for Dask to be deployed on.

    """
    if not nodes:
        raise ValueError("At least one node is required for Dask deployment.")

    log = get_logger(__name__)
    with ExitStack() as stack:
        stack.enter_context(stage_info(log,
                                       "Deploying Dask on %d nodes.",
                                       len(nodes)))

        first_node = nodes[0]
        assert isinstance(first_node, NodeInternal)
        config = first_node.config

        connect_to_each_node(nodes=nodes,
                             config=first_node.config)

        scheduler = deploy_scheduler_on_first_node(nodes)
        stack.enter_context(cancel_on_failure(scheduler))

        check_scheduler_reachable_from_nodes(nodes=nodes,
                                             scheduler=scheduler,
                                             config=config)

        workers = deploy_workers_on_each_node(nodes=nodes,
                                              scheduler=scheduler,
                                              stack=stack)

        valid_workers, nodes_to_redeploy = discard_invalid_workers(
            workers=workers,
            stack=stack)

        if nodes_to_redeploy:
            retries_with_no_improvement = 0
            retries_total = 0
            while nodes_to_redeploy:
                retries_total += 1

                with stage_info(log, "Redeploying workers on %d nodes.",
                                len(nodes_to_redeploy)):
                    redeployed_workers = deploy_workers_on_each_node(
                        nodes=nodes_to_redeploy,
                        scheduler=scheduler,
                        stack=stack)

                    redeploy_succeeded, nodes_to_redeploy = \
                        discard_invalid_workers(workers=redeployed_workers,
                                                stack=stack)

                    valid_workers.extend(redeploy_succeeded)

                    if redeploy_succeeded:
                        retries_with_no_improvement = 0
                    else:
                        retries_with_no_improvement += 1

                    if nodes_to_redeploy:
                        if retries_with_no_improvement >= 3:
                            raise RuntimeError(
                                "Failed to redeploy some nodes:"
                                " Too many retries with no improvement.")

                        if retries_total >= 10:
                            raise RuntimeError(
                                "Failed to redeploy some nodes:"
                                " Too many retries.")

        return DaskDeploymentImpl(scheduler=scheduler,
                                  workers=valid_workers)
