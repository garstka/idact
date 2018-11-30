"""This module contains the implementation of a Jupyter deployment interface.
"""

import webbrowser
from contextlib import ExitStack
from typing import Optional

from idact.core.jupyter_deployment import JupyterDeployment
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.deployment.generic_deployment import GenericDeployment
from idact.detail.helper.get_uuid import get_uuid
from idact.detail.helper.stage_info import stage_info
from idact.detail.log.get_logger import get_logger
from idact.detail.serialization.serializable import Serializable
from idact.detail.serialization.serializable_types import SerializableTypes
from idact.detail.tunnel.tunnel_internal import TunnelInternal


class JupyterDeploymentImpl(JupyterDeployment, Serializable):
    """Jupyter Notebook deployment on a node.

        :param deployment: Generic deployment of the notebook process.

        :param tunnel: SSH tunnel to the notebook.

        :param token: Authentication token.

        :param uuid: Unique deployment identifier.

    """

    def __init__(self,
                 deployment: GenericDeployment,
                 tunnel: TunnelInternal,
                 token: str,
                 uuid: Optional[str] = None):
        self._deployment = deployment
        self._tunnel = tunnel
        self._token = token
        self._uuid = uuid if uuid is not None else get_uuid()

    @property
    def local_port(self) -> int:
        return self._tunnel.here

    @property
    def uuid(self) -> str:
        """Unique deployment id."""
        return self._uuid

    @property
    def deployment(self) -> GenericDeployment:
        """Generic deployment of the notebook process."""
        return self._deployment

    @property
    def tunnel(self) -> TunnelInternal:
        """Tunnel to notebook server."""
        return self._tunnel

    @property
    def address(self) -> str:
        return "http://localhost:{local_port}/?token={token}".format(
            local_port=self.local_port,
            token=self._token)

    def open_in_browser(self):
        webbrowser.open(self.address)

    def cancel(self):
        log = get_logger(__name__)
        with ExitStack() as stack:
            stack.enter_context(stage_info(log,
                                           "Cancelling Jupyter deployment."))
            stack.enter_context(cancel_on_exit(self._deployment))
            self.cancel_local()

    def cancel_local(self):
        self._tunnel.close()

    def __str__(self):
        return "JupyterDeployment({local_port} -> {node}".format(
            local_port=self.local_port,
            node=self._deployment.node)

    def __repr__(self):
        return str(self)

    def serialize(self) -> dict:
        return {'type': str(SerializableTypes.JUPYTER_DEPLOYMENT_IMPL),
                'deployment': self._deployment.serialize(),
                'tunnel_there': self._tunnel.there,
                'tunnel_here': self._tunnel.here,
                'token': self._token}

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
