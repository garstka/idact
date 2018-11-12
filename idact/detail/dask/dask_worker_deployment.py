"""This module contains the implementation of a Dask worker deployment."""

from contextlib import ExitStack

from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.deployment.generic_deployment import GenericDeployment
from idact.detail.helper.stage_info import stage_info
from idact.detail.log.get_logger import get_logger
from idact.detail.tunnel.close_tunnel_on_exit import close_tunnel_on_exit
from idact.detail.tunnel.tunnel_internal import TunnelInternal


class DaskWorkerDeployment:
    """Deployment of a Dask worker on a node."""

    def __init__(self,
                 deployment: GenericDeployment,
                 bokeh_tunnel: TunnelInternal):
        self._deployment = deployment
        self._bokeh_tunnel = bokeh_tunnel

    @property
    def bokeh_tunnel(self) -> TunnelInternal:
        """Bokeh diagnostics server tunnel."""
        return self._bokeh_tunnel

    def cancel(self):
        """Cancels the scheduler deployment."""
        log = get_logger(__name__)
        with ExitStack() as stack:
            stack.enter_context(
                stage_info(log, "Cancelling worker deployment on %s.",
                           self._deployment.node.host))
            stack.enter_context(cancel_on_exit(self._deployment))
            stack.enter_context(close_tunnel_on_exit(self._bokeh_tunnel))

    @property
    def deployment(self) -> GenericDeployment:
        """Generic deployment."""
        return self._deployment
