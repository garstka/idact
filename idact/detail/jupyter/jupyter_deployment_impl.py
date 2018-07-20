import webbrowser

from idact.core.tunnel import Tunnel
from idact.core.nodes import Node
from idact.core.jupyter_deployment import JupyterDeployment
from idact.detail.deployment.generic_deployment import GenericDeployment


class JupyterDeploymentImpl(JupyterDeployment):
    """Jupyter notebook deployment on a node.

        :param node: Node the server was deployed on.

        :param deployment: Generic deployment of the notebook process.

        :param tunnel: SSH tunnel to the notebook.

    """

    def __init__(self,
                 node: Node,
                 deployment: GenericDeployment,
                 tunnel: Tunnel):
        self._node = node
        self._deployment = deployment
        self._tunnel = tunnel

    @property
    def local_port(self) -> int:
        return self._tunnel.here

    def open_in_browser(self):
        webbrowser.open("http://localhost:{local_port}".format(
            local_port=self.local_port))

    def cancel(self):
        self._tunnel.close()
        self._deployment.cancel()

    def __str__(self):
        return "{class_name}({local_port} -> {node})".format(
            class_name=self.__class__.__name__,
            local_port=self.local_port,
            node=self._node)

    def __repr__(self):
        return str(self)
