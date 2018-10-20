"""This module contains the internal cluster node interface."""
import datetime
from abc import abstractmethod

from typing import Optional, Callable, Any

import bitmath

from idact.core.nodes import Node
from idact.detail.config.client.client_cluster_config \
    import ClusterConfigImpl
from idact.detail.serialization.serializable import Serializable


class NodeInternal(Node, Serializable):
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

    @property
    @abstractmethod
    def cores(self) -> Optional[int]:
        """Returns the allocated node core count.
            Returns None for a node that was not allocated."""
        pass

    @property
    @abstractmethod
    def memory(self) -> Optional[bitmath.Byte]:
        """Returns the allocated node memory limit.
            Returns None for a node that was not allocated."""
        pass

    @property
    @abstractmethod
    def allocated_until(self) -> Optional[datetime.datetime]:
        """Datetime, when the allocation ends, or None if not allocated."""
        pass
