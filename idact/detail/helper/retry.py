from time import sleep

from typing import Callable, Any

from idact.detail.log.get_logger import get_logger


def retry(fun: Callable, retries: int, seconds_between_retries: int) -> Any:
    """Retries function call, if it throws an exception.

        :param fun:   Function to call.

        :param times: Times to call the function.

        :param seconds_between_retries: Time between calls.

    """
    log = get_logger(__name__)
    for i in range(0, retries + 1):
        try:
            return fun()
        except Exception as e:  # pylint: disable=broad-except
            if i >= retries:
                raise e
            log.warning("Exception: %s, retry %d/%d.",
                        str(e), i + 1, retries)
            sleep(seconds_between_retries)
