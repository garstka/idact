import logging
from contextlib import contextmanager


@contextmanager
def stage_info(log: logging.Logger, msg: str, *args, **kwargs):
    """A context manager that informs the user of the current stage.
        Entering the stage is logged with info level, failure with error level,
        and success with debug level.

        :param log: Logger to use.

        :param msg: Stage info message.

    """
    log.info(msg, *args, **kwargs)
    try:
        yield
    except Exception as e:  # noqa, pylint: disable=broad-except
        log.error("Failure: " + msg, *args, **kwargs)
        raise e
    log.debug("Success: " + msg, *args, **kwargs)


@contextmanager
def stage_debug(log: logging.Logger, msg: str, *args, **kwargs):
    """A context manager like :func:`.stage_info`, but it prints the entering
        stage message with debug level instead of info level.

        :param log: Logger to use.

        :param msg: Stage info message.

    """
    log.debug(msg, *args, **kwargs)
    try:
        yield
    except Exception as e:  # noqa, pylint: disable=broad-except
        log.error("Failure: " + msg, *args, **kwargs)
        raise e
    log.debug("Success: " + msg, *args, **kwargs)
