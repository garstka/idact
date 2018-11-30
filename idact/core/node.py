"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.Node`.
"""

from abc import ABC, abstractmethod

from typing import Optional

from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.node_resource_status import NodeResourceStatus
from idact.detail.tunnel.tunnel_internal import TunnelInternal


class Node(ABC):
    """Cluster node interface."""

    @abstractmethod
    def connect(self, timeout: Optional[int] = None):
        """Just connects to the node and executes a test command.
            Doing this explicitly is optional.

            :param timeout: Execution timeout.
        """
        pass

    @abstractmethod
    def run(self, command: str, timeout: Optional[int] = None) -> str:
        """Runs a command on the node. Returns the result as string.

            :param command: Command to run.

            :param timeout: Execution timeout.
        """
        pass

    @abstractmethod
    def tunnel(self,
               there: int,
               here: Optional[int] = None) -> TunnelInternal:
        """Creates an SSH tunnel from node to localhost.
            If the specified local port is taken, defaults to any port.

            :param there: Remote port to tunnel.

            :param here: Local port, or None for any port.
        """
        pass

    @abstractmethod
    def tunnel_ssh(self,
                   here: Optional[int] = None) -> TunnelInternal:
        """Creates an SSH tunnel to the SSH server on this node.
            If the specified local port is taken, defaults to any port.

            :param here: Local port, or None for any port.

        """
        pass

    @abstractmethod
    def deploy_notebook(self,
                        local_port: int = 8080) -> JupyterDeployment:
        """Deploys a Jupyter notebook on the node..

            :param local_port: Local notebook access port.
                               Default: 8080, or random if it's unavailable.

        """
        pass

    @property
    @abstractmethod
    def resources(self) -> NodeResourceStatus:
        """Returns the node resource status, like CPU and memory usage."""
        pass

    @property
    @abstractmethod
    def host(self) -> Optional[str]:
        """Hostname of the cluster node."""
        pass

    @property
    @abstractmethod
    def port(self) -> Optional[int]:
        """SSH port of the cluster node."""
        pass
