from abc import abstractmethod

from idact.core.config import ClusterConfig
from idact.core.tunnel import Tunnel


class TunnelInternal(Tunnel):
    """Internal tunnel interface."""

    @property
    @abstractmethod
    def config(self) -> ClusterConfig:
        pass
