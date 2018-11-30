from typing import Dict

from idact.core.config import RetryConfig
from idact.core.get_default_retries import get_default_retries
from idact.core.retry import Retry
from idact.detail.config.client.retry_config_impl import RetryConfigImpl


# pylint: disable=bad-continuation
def provide_defaults_for_retries(
    retries: Dict[Retry, RetryConfig]) -> Dict[Retry, RetryConfig]:  # noqa
    """Add defaults for entries not in `retries`. Returns mutated `retries`.

        :param retries: Retries config to provide defaults for.

    """
    for key, defaults in get_default_retries().items():
        if key not in retries:
            retries[key] = RetryConfigImpl(
                count=defaults.count,
                seconds_between=defaults.seconds_between)

    return retries
