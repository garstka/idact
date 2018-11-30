"""This module contains the implementation of a global logger provider."""

import logging
import sys

from idact.detail.log.debug_log_filter import DebugLogFilter


class LoggerProvider:
    """Stores global log level and provides loggers with
        proper level and handler.

        Log level is managed by :class:`.EnvironmentProvider`
        and :func:`.set_log_level`.

    """
    _state = {}

    def __init__(self):
        if LoggerProvider._state:
            self.__dict__ = LoggerProvider._state
            return

        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")

        self._stream_handler = logging.StreamHandler(stream=sys.stdout)
        self._stream_handler.setFormatter(formatter)

        self._file_handler = logging.FileHandler(filename='idact.log',
                                                 mode='w')
        self._file_handler.setFormatter(formatter)

        self._handlers = [self._stream_handler,
                          self._file_handler]

        self._log_level = None
        self.log_level = logging.INFO

        self._debug_log_filters = [DebugLogFilter()]

        LoggerProvider._state = self.__dict__

    @property
    def log_level(self) -> int:
        """Log level for console output."""
        return self._log_level

    @log_level.setter
    def log_level(self, level: int):
        self._stream_handler.setLevel(level)
        self._log_level = level

    def get_logger(self, name: str) -> logging.Logger:
        """Returns a new logger with a DEBUG log level.
            Note: Level may be higher in handlers.

            :param name: Logger name.

        """
        logger = logging.getLogger(name)
        logger.setLevel(logging.DEBUG)
        logger.handlers = self._handlers
        return logger

    def get_debug_logger(self, name: str) -> logging.Logger:
        """Returns a logger with a DEBUG log level,
            that will also log everything with a DEBUG level.

            :param name: Logger name.

        """
        logger = self.get_logger(name)
        logger.filters = self._debug_log_filters

        return logger
