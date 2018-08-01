import webbrowser

from idact.core.tunnel import Tunnel
from idact.core.nodes import Node
from idact.core.jupyter_deployment import JupyterDeployment
from idact.detail.deployment.generic_deployment import GenericDeployment
from idact.detail.helper.remove_runtime_dir import remove_runtime_dir


class JupyterDeploymentImpl(JupyterDeployment):
    """Jupyter notebook deployment on a node.

        :param node: Node the server was deployed on.

        :param deployment: Generic deployment of the notebook process.

        :param tunnel: SSH tunnel to the notebook.

        :param token: Authentication token.

        :param runtime_dir: Runtime dir to remove.

    """

    def __init__(self,
                 node: Node,
                 deployment: GenericDeployment,
                 tunnel: Tunnel,
                 token: str,
                 runtime_dir: str):
        self._node = node
        self._deployment = deployment
        self._tunnel = tunnel
        self._token = token
        self._runtime_dir = runtime_dir

    @property
    def local_port(self) -> int:
        return self._tunnel.here

    def open_in_browser(self):
        webbrowser.open("http://localhost:{local_port}/?token={token}".format(
            local_port=self.local_port,
            token=self._token))

    def cancel(self):
        try:
            self._tunnel.close()
        finally:
            try:
                self._deployment.cancel()
            finally:
                remove_runtime_dir(node=self._node,
                                   runtime_dir=self._runtime_dir)

    def __str__(self):
        return "JupyterDeployment({local_port} -> {node})".format(
            local_port=self.local_port,
            node=self._node)

    def __repr__(self):
        return str(self)
