import webbrowser

from idact.core.tunnel import Tunnel
from idact.core.nodes import Node
from idact.core.jupyter_deployment import JupyterDeployment


class JupyterDeploymentImpl(JupyterDeployment):
    """Jupyter notebook deployment on a node.

        :param node: Node the server was deployed on.
    """

    def __init__(self,
                 node: Node,
                 tunnel: Tunnel):
        self._node = node
        self._tunnel = tunnel

    @property
    def local_port(self) -> int:
        """The local access port."""
        return self._tunnel.here

    def open_in_browser(self):
        """Opens the notebook server in the local browser."""
        webbrowser.open("http://localhost:{local_port}".format(
            local_port=self.local_port))

    def cancel(self):
        """Closes the notebook server."""
        self._tunnel.close()
        # Only temporary and non-portable:
        self._node.run("killall -u $USER jupyterhub")
        self._node.run("pkill -f \"/usr/bin/python3.6 /usr/bin/jupyterhub\"")
        self._node.run("pkill -f \"node /usr/bin/configurable-http-proxy\"")

    def __str__(self):
        return "{class_name}({local_port} -> {node})".format(
            class_name=self.__class__.__name__,
            local_port=self.local_port,
            node=self._node)

    def __repr__(self):
        return str(self)
