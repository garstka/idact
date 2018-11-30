"""This module contains a function for setting the log level for paramiko."""
import logging

from idact.detail.log.get_logger import get_debug_logger

PARAMIKO_LOG_LEVEL = logging.WARNING


def set_paramiko_log_level():
    """Sets the log level for paramiko."""
    transport = get_debug_logger('paramiko.transport')
    transport.setLevel(PARAMIKO_LOG_LEVEL)
