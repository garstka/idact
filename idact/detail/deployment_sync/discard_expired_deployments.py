from datetime import timedelta

from idact.detail.deployment_sync.deployment_definitions import \
    DeploymentDefinitions
from idact.detail.helper.stage_info import stage_debug
from idact.detail.helper.utc_now import utc_now
from idact.detail.log.get_logger import get_logger

DISCARD_DELTA_SECONDS = 30
"""Discard deployments this number of seconds before
    the actual expiration date."""


# pylint: disable=bad-continuation
def discard_expired_deployments(
    deployments: DeploymentDefinitions) -> DeploymentDefinitions:  # noqa
    """Returns a new object that does not contain deployments
        that have expired, or will expire in the near future.

        :param deployments: Deployments to examine.

    """
    log = get_logger(__name__)

    with stage_debug(log, "Discarding expired deployments."):
        now = utc_now()
        log.debug("Now: %s", now)
        log.debug("Will discard after the %d second mark"
                  " before the expiration date.",
                  DISCARD_DELTA_SECONDS)

        discard_now = utc_now() + timedelta(seconds=DISCARD_DELTA_SECONDS)

        unexpired_nodes = {}
        for uuid, node in deployments.nodes.items():
            if node.expiration_date < discard_now:
                log.warning("Discarding a synchronized allocation deployment,"
                            " because it has expired: %s", uuid)
            else:
                unexpired_nodes[uuid] = node

        unexpired_jupyter_deployments = {}
        for uuid, jupyter in deployments.jupyter_deployments.items():
            if jupyter.expiration_date < discard_now:
                log.warning("Discarding a Jupyter deployment,"
                            " because it has expired: %s", uuid)
            else:
                unexpired_jupyter_deployments[uuid] = jupyter

        unexpired_dask_deployments = {}
        for uuid, dask in deployments.dask_deployments.items():
            if dask.expiration_date < discard_now:
                log.warning("Discarding a Dask deployment,"
                            " because it has expired: %s", uuid)
            else:
                unexpired_dask_deployments[uuid] = dask

        return DeploymentDefinitions(
            nodes=unexpired_nodes,
            jupyter_deployments=unexpired_jupyter_deployments,
            dask_deployments=unexpired_dask_deployments)
