"""This module contains the implementation of a Dask worker deployment."""

from contextlib import ExitStack

from idact.core.config import ClusterConfig
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.deployment.deserialize_generic_deployment import \
    deserialize_generic_deployment
from idact.detail.deployment.generic_deployment import GenericDeployment
from idact.detail.helper.stage_info import stage_info
from idact.detail.log.get_logger import get_logger
from idact.detail.serialization.serializable import Serializable
from idact.detail.serialization.serializable_types import SerializableTypes
from idact.detail.tunnel.tunnel_internal import TunnelInternal


class DaskWorkerDeployment(Serializable):
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
            self.cancel_local()

    def cancel_local(self):
        """Closes the tunnel, but does not cancel the deployment."""
        self._bokeh_tunnel.close()

    @property
    def deployment(self) -> GenericDeployment:
        """Generic deployment."""
        return self._deployment

    def serialize(self) -> dict:
        return {'type': str(SerializableTypes.DASK_WORKER_DEPLOYMENT),
                'deployment': self._deployment.serialize(),
                'bokeh_tunnel_here': self._bokeh_tunnel.here,
                'bokeh_tunnel_there': self._bokeh_tunnel.there}

    @staticmethod
    def deserialize(config: ClusterConfig,
                    serialized: dict) -> 'DaskWorkerDeployment':
        try:
            assert serialized['type'] == str(
                SerializableTypes.DASK_WORKER_DEPLOYMENT)

            deployment = deserialize_generic_deployment(
                config=config,
                serialized=serialized['deployment'])
            bokeh_tunnel = deployment.node.tunnel(
                there=serialized['bokeh_tunnel_there'],
                here=serialized['bokeh_tunnel_here'])
            return DaskWorkerDeployment(
                deployment=deployment,
                bokeh_tunnel=bokeh_tunnel)
        except KeyError as e:
            raise RuntimeError("Unable to deserialize.") from e

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
