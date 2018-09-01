"""This module contains the implementation of a global environment provider."""

from typing import Optional

from idact.detail.environment.environment import Environment
from idact.detail.environment.environment_serialization import \
    deserialize_environment_from_file
from idact.detail.log.logger_provider import LoggerProvider


class EnvironmentProvider:
    """Creates and stores the global environment.

        :param initial_environment: Optionally use this environment instead
                                    of loading from a file on first access.

    """

    _state = {}

    def __init__(self, initial_environment: Optional[Environment] = None):
        if EnvironmentProvider._state:
            self.__dict__ = EnvironmentProvider._state
            return
        self._set_global_environment(initial_environment)
        EnvironmentProvider._state = self.__dict__

    @property
    def environment(self) -> Environment:
        """Returns the current environment.
           Tries to load it from file if there is none.
        """
        if self._environment is None:
            new_environment = deserialize_environment_from_file(
                ignore_if_missing=True)
            self._set_global_environment(new_environment)

        return self._environment

    @environment.setter
    def environment(self, value: Environment):
        """Sets the current environment.

            :param value: New environment.
        """
        self._set_global_environment(value)

    def _set_global_environment(self, value: Optional[Environment]):
        """Sets the current environment and log level.

            :param value: Environment to set as current.

        """
        self._environment = value
        if value is not None:
            LoggerProvider().log_level = self._environment.config.log_level
