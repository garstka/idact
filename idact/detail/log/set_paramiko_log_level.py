"""This module contains a function for setting the log level for paramiko."""
import logging


def set_paramiko_log_level(level: int):
    """Sets the log level for paramiko.

        :param level: Log level.

    """
    logger = logging.getLogger("paramiko")
    logger.setLevel(level)
