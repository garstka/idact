"""This module contains a function for retrying a function call on exception.
"""

from time import sleep

from typing import Callable, Any

from idact.core.config import ClusterConfig
from idact.core.retry import Retry
from idact.detail.log.get_logger import get_logger


def format_retry_failed_message(name: Retry,
                                count: int,
                                seconds_between: int) -> str:
    """Formats a retry failed message.

        :param name: Retry action name.

        :param count: Configured retry count.

        :param seconds_between: Seconds between retries.

    """
    return (
        "Retried and failed: config.retries[{name!s}].{{count={count}, "
        "seconds_between={seconds_between}}}".format(
            name=name,
            count=count,
            seconds_between=seconds_between))


def retry_with_config(fun: Callable,
                      name: Retry,
                      config: ClusterConfig,
                      multiplier: int = 1):
    """See :func:`.retry`, but timeouts are taken from config.

        :param fun:    Function to call.
        :param name:   Timeout name.
        :param config: Config to take timeouts from.
        :param multiplier: Retry count multiplier.
    """
    retries = config.retries[name]
    count = retries.count
    seconds_between = retries.seconds_between
    try:
        return retry(fun=fun,
                     retries=count * multiplier,
                     seconds_between_retries=seconds_between)
    except Exception as e:  # pylint: disable=broad-except
        log = get_logger(__name__)
        message = format_retry_failed_message(name=name,
                                              count=count,
                                              seconds_between=seconds_between)
        log.info(message)
        log.debug("Retry multiplier was %d.", multiplier)
        raise RuntimeError(message) from e


def retry(fun: Callable, retries: int, seconds_between_retries: int) -> Any:
    """Retries the function call, if it throws an exception.

        Returns the function return value, if it does not throw.
        If all retries fail, re-raises the last raised exception.

        :param fun:   Function to call.

        :param retries: Number of retries.

        :param seconds_between_retries: Time to sleep before each retry.

    """
    log = get_logger(__name__)
    for i in range(0, retries + 1):
        try:
            return fun()
        except Exception as e:  # pylint: disable=broad-except
            if i >= retries:
                raise e
            log.debug("%s, retry %d/%d.",
                      str(e), i + 1, retries)
            sleep(seconds_between_retries)
