"""This module contains a function for setting the log level for Fabric."""
import logging
import sys
from contextlib import contextmanager
from io import StringIO

import fabric.state

from idact.detail.log.get_logger import get_logger

FABRIC_LOGGER_NAME = "idact.fabric"
STDOUT_FILENO = 1
STDERR_FILENO = 2


class LoggerOut(StringIO):
    """Replacement for stdout, stderr that uses a logger.

        :param logger: Logger to use.

        :param fileno: File number that may be required by Fabric.

    """

    def __init__(self, logger: logging.Logger, fileno: int):
        super().__init__()
        self._logger = logger
        self._fileno = fileno

    def write(self, message):
        message = message.rstrip()
        if message:
            self._logger.debug(message)

    def fileno(self) -> int:
        """Returns the file number for corresponding output."""
        return self._fileno


@contextmanager
def capture_fabric_output_to_log():
    """Turns on all Fabric output and replaces `sys.stdout`, `sys.stderr`
        with a logger DEBUG output.

    """
    saved = {group: fabric.state.output[group]
             for group in ['status',
                           'aborts',
                           'warnings',
                           'running',
                           'stdout',
                           'stderr',
                           'user',
                           'debug',
                           'exceptions']}
    for group in saved.keys():
        fabric.state.output[group] = True

    logger = get_logger(FABRIC_LOGGER_NAME)
    saved_stdout = sys.stdout
    saved_stderr = sys.stderr
    replacement_stdout = LoggerOut(logger=logger, fileno=STDOUT_FILENO)
    replacement_stderr = LoggerOut(logger=logger, fileno=STDERR_FILENO)
    try:
        sys.stdout = replacement_stdout
        sys.stderr = replacement_stderr
        yield
    finally:
        sys.stderr = saved_stderr
        sys.stdout = saved_stdout
        for group, show in saved.items():
            fabric.state.output[group] = show
