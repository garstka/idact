from contextlib import ExitStack

from idact.core.tunnel import Tunnel
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.deployment.generic_deployment import GenericDeployment
from idact.detail.tunnel.close_tunnel_on_exit import close_tunnel_on_exit


class DaskSchedulerDeployment:
    """Deployment of a Dask scheduler on a node."""

    def __init__(self,
                 deployment: GenericDeployment,
                 tunnel: Tunnel,
                 bokeh_tunnel: Tunnel,
                 address: str):
        self._deployment = deployment
        self._tunnel = tunnel
        self._bokeh_tunnel = bokeh_tunnel
        self._address = address

    @property
    def local_address(self) -> str:
        """Local address of the scheduler (tunnelled)."""
        return "tcp://localhost:{}".format(self._tunnel.here)

    @property
    def address(self) -> str:
        """Remote address of the scheduler for workers."""
        return self._address

    @property
    def bokeh_tunnel(self) -> Tunnel:
        """Bokeh diagnostics server tunnel."""
        return self._bokeh_tunnel

    def cancel(self):
        """Cancels the scheduler deployment."""
        with ExitStack() as stack:
            stack.enter_context(cancel_on_exit(self._deployment))
            stack.enter_context(close_tunnel_on_exit(self._tunnel))
            stack.enter_context(close_tunnel_on_exit(self._bokeh_tunnel))
