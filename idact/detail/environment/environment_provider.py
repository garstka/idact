"""This module contains the implementation of a global environment provider."""

from typing import Optional

from fabric.state import env

from idact.detail.environment.environment import Environment
from idact.detail.environment.environment_impl import EnvironmentImpl
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
            new_environment = EnvironmentImpl()
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
            env.connection_attempts = 3
            env.gss_auth = False
            env.gss_deleg = False
            env.gss_kex = False
            env.keepalive = 30
            env.no_agent = True
            env.no_keys = True  # only explicit keys
            env.rcfile = None
            env.ssh_config_path = None
            env.timeout = 15
            env.use_ssh_config = False
            env.warn_only = False
