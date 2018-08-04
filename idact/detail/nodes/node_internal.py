from abc import abstractmethod

from typing import Optional, Callable, Any

from idact.core.nodes import Node
from idact.detail.config.client.client_cluster_config \
    import ClusterConfigImpl


class NodeInternal(Node):
    """Node interface for internal use."""

    @abstractmethod
    def run_impl(self,
                 command: str,
                 timeout: Optional[int] = None,
                 install_keys: bool = False) -> str:
        """Internal run.

            :param command: See :meth:`.Node.run`

            :param timeout: See :meth:`.Node.run`

            :param install_keys: See :meth:`.NodeInternal.run_task`

        """
        pass

    @abstractmethod
    def run_task(self,
                 task: Callable,
                 install_keys: bool = False) -> Any:
        """Internal run task.

            :param task: Fabric task to run.

            :param install_keys: If True, shared SSH keys will be installed
                            after authentication (see :func:`.install_key`,
                            :func:`.install_shared_home_key`).

        """
        pass

    @property
    @abstractmethod
    def config(self) -> ClusterConfigImpl:
        """Client cluster config."""
        pass
