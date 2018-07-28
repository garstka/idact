from logging import DEBUG

from fabric.context_managers import show, hide


def set_fabric_log_level(level: int):
    """Sets the log level for Fabric given idact log level.
       If level <= DEBUG, full Fabric output is shown.
       Otherwise, all Fabric output is hidden.

        :param level: Log level.
    """
    if level <= DEBUG:
        show('everything').__enter__()  # pylint: disable=no-member
    else:
        hide('everything').__enter__()  # pylint: disable=no-member
