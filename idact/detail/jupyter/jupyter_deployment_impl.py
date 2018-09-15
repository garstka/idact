"""This module contains the implementation of a Jupyter deployment interface.
"""

import webbrowser
from contextlib import ExitStack

from idact.core.tunnel import Tunnel
from idact.core.nodes import Node
from idact.core.jupyter_deployment import JupyterDeployment
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.deployment.generic_deployment import GenericDeployment
from idact.detail.tunnel.close_tunnel_on_exit import close_tunnel_on_exit


class JupyterDeploymentImpl(JupyterDeployment):
    """Jupyter Notebook deployment on a node.

        :param node: Node the server was deployed on.

        :param deployment: Generic deployment of the notebook process.

        :param tunnel: SSH tunnel to the notebook.

        :param token: Authentication token.

    """

    def __init__(self,
                 node: Node,
                 deployment: GenericDeployment,
                 tunnel: Tunnel,
                 token: str):
        self._node = node
        self._deployment = deployment
        self._tunnel = tunnel
        self._token = token

    @property
    def local_port(self) -> int:
        return self._tunnel.here

    def open_in_browser(self):
        webbrowser.open("http://localhost:{local_port}/?token={token}".format(
            local_port=self.local_port,
            token=self._token))

    def cancel(self):
        with ExitStack() as stack:
            stack.enter_context(cancel_on_exit(self._deployment))
            stack.enter_context(close_tunnel_on_exit(self._tunnel))

    def __str__(self):
        return "JupyterDeployment({local_port} -> {node})".format(
            local_port=self.local_port,
            node=self._node)

    def __repr__(self):
        return str(self)
