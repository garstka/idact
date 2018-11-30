"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.SetupActionsConfig`, :class:`.ClusterConfig`.
"""

from abc import ABC, abstractmethod
from typing import Optional, List, Dict
from idact.core.auth import AuthMethod
from idact.core.retry import Retry


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

    @property
    @abstractmethod
    def dask(self) -> List[str]:
        """Commands to run before deployment of Dask."""
        pass

    @dask.setter
    @abstractmethod
    def dask(self, value: List[str]):
        pass


class RetryConfig:
    """Retry config for an action."""

    @property
    @abstractmethod
    def count(self) -> int:
        """Number of retries."""
        pass

    @count.setter
    @abstractmethod
    def count(self, value: int):
        pass

    @property
    @abstractmethod
    def seconds_between(self) -> int:
        """Seconds between retries."""
        pass

    @seconds_between.setter
    @abstractmethod
    def seconds_between(self, value: int):
        pass


class ClusterConfig(ABC):
    """Client-side cluster config."""

    @property
    @abstractmethod
    def host(self) -> str:
        """Cluster hostname."""
        pass

    @host.setter
    @abstractmethod
    def host(self, value: str):
        pass

    @property
    @abstractmethod
    def port(self) -> int:
        """Cluster SSH port number."""
        pass

    @port.setter
    @abstractmethod
    def port(self, value: int):
        pass

    @property
    @abstractmethod
    def user(self) -> str:
        """Cluster user to log in and run commands as."""
        pass

    @user.setter
    @abstractmethod
    def user(self, value: str):
        pass

    @property
    @abstractmethod
    def auth(self) -> AuthMethod:
        """Authentication method."""
        pass

    @auth.setter
    @abstractmethod
    def auth(self, value: AuthMethod):
        pass

    @property
    @abstractmethod
    def key(self) -> Optional[str]:
        """Private key path (if applicable).
           It will be auto-generated if needed."""
        pass

    @key.setter
    @abstractmethod
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

    @disable_sshd.setter
    @abstractmethod
    def disable_sshd(self, value: bool):
        pass

    @property
    @abstractmethod
    def setup_actions(self) -> SetupActionsConfig:
        """Commands to run before deployment."""
        pass

    @property
    @abstractmethod
    def scratch(self) -> str:
        """Absolute path to a high-performance filesystem for temporary
           computation data, or an environment variable that contains it."""
        pass

    @scratch.setter
    @abstractmethod
    def scratch(self, value: str):
        pass

    @property
    @abstractmethod
    def retries(self) -> Dict[Retry, RetryConfig]:
        """Retry config by retried action name."""
        pass

    @property
    @abstractmethod
    def use_jupyter_lab(self) -> bool:
        """Use Jupyter Lab instead of Jupyter Notebook."""
        pass

    @use_jupyter_lab.setter
    @abstractmethod
    def use_jupyter_lab(self, value: bool):
        pass
