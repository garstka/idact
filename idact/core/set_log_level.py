"""Contents of this module are intended to be imported into
   the top-level package.

   See :func:`.set_log_level`.
"""

from idact.detail.environment.environment_provider import EnvironmentProvider
from idact.detail.log.logger_provider import LoggerProvider


def set_log_level(level: int):
    """Sets log level for idact loggers.

        If the log level is lower or equal to DEBUG, Fabric logs are also
        shown, otherwise they are hidden.

        :param level: May be one of CRITICAL, FATAL, ERROR, WARNING,
                      WARN, INFO, DEBUG, NOTSET. Default: INFO

    """
    environment = EnvironmentProvider().environment
    environment.set_log_level(level=level)
    LoggerProvider().log_level = level
