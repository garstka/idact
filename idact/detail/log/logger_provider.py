import logging
import sys


class LoggerProvider:
    """Stores global log level and provides loggers with
        proper level and handler.

        Log level is managed by :class:`.Environment`.

    """
    _state = {}

    def __init__(self):
        if LoggerProvider._state:
            self.__dict__ = LoggerProvider._state
            return

        self.log_level = logging.INFO

        handler = logging.StreamHandler(stream=sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s %(levelname)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S")
        handler.setFormatter(formatter)
        self._handlers = [handler]

        LoggerProvider._state = self.__dict__

    def get_logger(self, name: str) -> logging.Logger:
        """Returns a new logger.

            :param name: Logger name.

        """
        logger = logging.getLogger(name)
        logger.setLevel(self.log_level)
        logger.handlers = self._handlers
        return logger
