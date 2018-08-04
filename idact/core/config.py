"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.SetupActionsConfig`, :class:`.ClusterConfig`.
"""

from abc import ABC, abstractmethod
from typing import Optional, List
from idact.core.auth import AuthMethod


class SetupActionsConfig:
    """Commands to run before deployment."""

    @property
    @abstractmethod
    def jupyter(self) -> List[str]:
        """Commands to run before deployment of Jupyter Notebook."""
        pass

    @jupyter.setter
    @abstractmethod
    def jupyter(self, value: List[str]):
        pass


class ClusterConfig(ABC):
    """Client-side cluster config."""

    @property
    @abstractmethod
    def host(self) -> str:
        """Cluster hostname."""
        pass

    @property
    @abstractmethod
    def port(self) -> int:
        """Cluster SSH port number."""
        pass

    @property
    @abstractmethod
    def user(self) -> str:
        """Cluster user to log in and run commands as."""
        pass

    @property
    @abstractmethod
    def auth(self) -> AuthMethod:
        """Authentication method."""
        pass

    @property
    @abstractmethod
    def key(self) -> Optional[str]:
        """Private key path (if applicable).
           It will be auto-generated if needed."""
        pass

    @key.setter
    def key(self, value: Optional[str]):
        pass

    @property
    @abstractmethod
    def install_key(self) -> bool:
        """True, if the key should be installed on cluster before use."""
        pass

    @install_key.setter
    @abstractmethod
    def install_key(self, value: bool):
        pass

    @property
    @abstractmethod
    def disable_sshd(self) -> bool:
        """Disables sshd server as an entry point for all nodes."""
        pass

    @property
    @abstractmethod
    def setup_actions(self) -> SetupActionsConfig:
        """Commands to run before deployment."""
        pass
