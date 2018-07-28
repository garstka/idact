from logging import DEBUG

import fabric.state


def set_fabric_log_level(level: int):
    """Sets the log level for Fabric given idact log level.
       If level <= DEBUG, full Fabric output is shown.
       Otherwise, all Fabric output is hidden.

        :param level: Log level.
    """
    show = level <= DEBUG
    for group in ['warnings', 'running', 'user', 'output', 'exceptions']:
        fabric.state.output[group] = show
