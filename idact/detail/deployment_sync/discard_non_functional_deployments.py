from idact.core.synchronized_deployments import SynchronizedDeployments
from idact.detail.deployment_sync.synchronized_deployments_impl import \
    SynchronizedDeploymentsImpl
from idact.detail.helper.stage_info import stage_debug
from idact.detail.log.get_logger import get_logger


# pylint: disable=bad-continuation
def discard_non_functional_deployments(
    deployments: SynchronizedDeployments) -> SynchronizedDeployments:  # noqa
    """Discards deployments that were not expired, but are no longer
        functional, e.g. were cancelled."""

    log = get_logger(__name__)
    all_nodes = []
    for nodes in deployments.nodes:
        with stage_debug(log, "Checking whether allocation deployment"
                              " is functional: %s.", nodes):
            nodes_functional = not nodes.waited or nodes.running()

        if nodes_functional:
            all_nodes.append(nodes)
        else:
            log.warning("Discarding an allocation deployment, "
                        " because it is no longer functional: %s.", nodes)

    return SynchronizedDeploymentsImpl(nodes=all_nodes)
