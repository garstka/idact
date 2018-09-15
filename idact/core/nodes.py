"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.Node`, :class:`.Nodes`.
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from typing import Optional

from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.node_resource_status import NodeResourceStatus
from idact.core.tunnel import Tunnel


class Node(ABC):
    """Cluster node interface."""

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
               here: Optional[int] = None) -> Tunnel:
        """Creates an SSH tunnel from node to localhost.

            :param there: Remote port to tunnel.

            :param here: Local port, or None for any port.
        """
        pass

    @abstractmethod
    def deploy_notebook(self,
                        local_port: int = 8080) -> JupyterDeployment:
        """Deploys a Jupyter notebook on the node..

            :param local_port: Local notebook access port.
        """
        pass

    @property
    @abstractmethod
    def resources(self) -> NodeResourceStatus:
        """Returns the node resource status, like CPU and memory usage."""
        pass


class Nodes(Sequence):
    """Collection of cluster nodes allocated together."""

    @abstractmethod
    def wait(self,
             timeout: Optional[float] = None):
        """Waits until the nodes are allocated.

            :param timeout: Maximum number of seconds to wait for allocation.
                            None is treated as no limit.

            :raises RuntimeException: On error.

            :raises TimeoutException: On timeout.
        """
        pass

    @abstractmethod
    def cancel(self):
        """Deallocates the nodes or cancels the allocation request."""
        pass

    @abstractmethod
    def running(self) -> bool:
        """Returns True if the nodes are running."""
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __getitem__(self, i: int) -> Node:
        pass

    @abstractmethod
    def __contains__(self, x: object) -> bool:
        pass
