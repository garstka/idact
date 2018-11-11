from idact.core.synchronized_deployments import SynchronizedDeployments
from idact.detail.deployment_sync.synchronized_deployments_impl import \
    SynchronizedDeploymentsImpl
from idact.detail.helper.stage_info import stage_debug
from idact.detail.jupyter.jupyter_deployment_impl import JupyterDeploymentImpl
from idact.detail.log.get_logger import get_logger
from idact.detail.tunnel.validate_tunnel_http_connection import \
    validate_tunnel_http_connection


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
            log.info("Discarding an allocation deployment,"
                     " because it is no longer functional: %s.", nodes)

    all_jupyter_deployments = []
    for jupyter in deployments.jupyter_deployments:
        jupyter_impl = jupyter
        assert isinstance(jupyter_impl, JupyterDeploymentImpl)
        with stage_debug(log, "Checking whether Jupyter deployment"
                              " is functional: %s.", jupyter_impl):
            try:
                validate_tunnel_http_connection(tunnel=jupyter_impl.tunnel)
                all_jupyter_deployments.append(jupyter_impl)
            except Exception:  # pylint: disable=broad-except
                log.info("Discarding a Jupyter deployment,"
                         " because it is no longer functional: %s.",
                         jupyter_impl)
                log.debug("Exception", exc_info=1)
                with stage_debug(log,
                                 "Cancelling tunnel to discarded notebook."):
                    jupyter_impl.cancel_local()

    return SynchronizedDeploymentsImpl(
        nodes=all_nodes,
        jupyter_deployments=all_jupyter_deployments)
