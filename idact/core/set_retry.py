from idact.core.config import RetryConfig
from idact.detail.config.client.retry_config_impl import RetryConfigImpl


def set_retry(count: int, seconds_between: int = 5) -> RetryConfig:
    """Returns a retry config value for a :class:`.Retry` key.

        :param count: Number of retries.

        :param seconds_between: Seconds between retries.

    """
    return RetryConfigImpl(count=count, seconds_between=seconds_between)
