"""This module contains the implementation of a Dask scheduler deployment."""

from contextlib import ExitStack

from idact.core.config import ClusterConfig
from idact.core.tunnel import Tunnel
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.deployment.deserialize_generic_deployment import \
    deserialize_generic_deployment
from idact.detail.deployment.generic_deployment import GenericDeployment
from idact.detail.helper.stage_info import stage_info
from idact.detail.log.get_logger import get_logger
from idact.detail.serialization.serializable import Serializable
from idact.detail.serialization.serializable_types import SerializableTypes
from idact.detail.tunnel.close_tunnel_on_exit import close_tunnel_on_exit
from idact.detail.tunnel.tunnel_internal import TunnelInternal


class DaskSchedulerDeployment(Serializable):
    """Deployment of a Dask scheduler on a node."""

    def __init__(self,
                 deployment: GenericDeployment,
                 tunnel: Tunnel,
                 bokeh_tunnel: TunnelInternal,
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
    def bokeh_tunnel(self) -> TunnelInternal:
        """Bokeh diagnostics server tunnel."""
        return self._bokeh_tunnel

    @property
    def deployment(self) -> GenericDeployment:
        """Generic deployment."""
        return self._deployment

    def cancel(self):
        """Cancels the scheduler deployment."""
        log = get_logger(__name__)
        with ExitStack() as stack:
            stack.enter_context(
                stage_info(log, "Cancelling scheduler deployment on %s.",
                           self._deployment.node.host))
            stack.enter_context(cancel_on_exit(self._deployment))
            self.cancel_local()

    def cancel_local(self):
        """Closes the tunnels, but does not cancel the deployment."""
        with ExitStack() as stack:
            stack.enter_context(close_tunnel_on_exit(self._tunnel))
            stack.enter_context(close_tunnel_on_exit(self._bokeh_tunnel))

    def serialize(self) -> dict:
        return {'type': str(SerializableTypes.DASK_SCHEDULER_DEPLOYMENT),
                'deployment': self._deployment.serialize(),
                'tunnel_here': self._tunnel.here,
                'tunnel_there': self._tunnel.there,
                'bokeh_tunnel_here': self._bokeh_tunnel.here,
                'bokeh_tunnel_there': self._bokeh_tunnel.there,
                'address': self._address}

    @staticmethod
    def deserialize(config: ClusterConfig,
                    serialized: dict) -> 'DaskSchedulerDeployment':
        try:
            assert serialized['type'] == str(
                SerializableTypes.DASK_SCHEDULER_DEPLOYMENT)

            deployment = deserialize_generic_deployment(
                config=config,
                serialized=serialized['deployment'])
            tunnel = deployment.node.tunnel(
                there=serialized['tunnel_there'],
                here=serialized['tunnel_here'])
            bokeh_tunnel = deployment.node.tunnel(
                there=serialized['bokeh_tunnel_there'],
                here=serialized['bokeh_tunnel_here'])
            return DaskSchedulerDeployment(
                deployment=deployment,
                tunnel=tunnel,
                bokeh_tunnel=bokeh_tunnel,
                address=serialized['address'])
        except KeyError as e:
            raise RuntimeError("Unable to deserialize.") from e

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
