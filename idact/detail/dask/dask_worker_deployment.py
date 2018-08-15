from contextlib import ExitStack

from idact.core.tunnel import Tunnel
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.deployment.generic_deployment import GenericDeployment
from idact.detail.tunnel.close_tunnel_on_exit import close_tunnel_on_exit


class DaskWorkerDeployment:
    """Deployment of a Dask worker on a node."""

    def __init__(self,
                 deployment: GenericDeployment,
                 bokeh_tunnel: Tunnel):
        self._deployment = deployment
        self._bokeh_tunnel = bokeh_tunnel

    @property
    def bokeh_tunnel(self) -> Tunnel:
        """Bokeh diagnostics server tunnel."""
        return self._bokeh_tunnel

    def cancel(self):
        """Cancels the scheduler deployment."""
        with ExitStack() as stack:
            stack.enter_context(cancel_on_exit(self._deployment))
            stack.enter_context(close_tunnel_on_exit(self._bokeh_tunnel))
