from typing import Optional

from idact.detail.environment.environment import Environment
from idact.detail.environment.environment_serialization import \
    deserialize_environment_from_file


class EnvironmentProvider:
    """Creates and stores the global environment."""

    _state = {}

    def __init__(self, initial_environment: Optional[Environment] = None):
        if EnvironmentProvider._state:
            self.__dict__ = EnvironmentProvider._state
            return
        self._environment = initial_environment
        EnvironmentProvider._state = self.__dict__

    @property
    def environment(self) -> Environment:
        """Returns the current environment.
           Tries to load it if there is none."""
        if self._environment is None:
            self.environment = deserialize_environment_from_file()
        return self._environment

    @environment.setter
    def environment(self, value: Environment):
        """Sets the current environment.

            :param value: New environment.
        """
        self._environment = value
