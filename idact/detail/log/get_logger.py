"""This module contains a function for getting a logger from a global provider.
"""

import logging

from idact.detail.log.logger_provider import LoggerProvider


def get_logger(name: str) -> logging.Logger:
    """Returns a logger with the proper logging level set.

        See :class:`.LoggerProvider`.

        :param name: Logger name, e.g. `__name__` of the caller.

    """
    return LoggerProvider().get_logger(name=name)
