from typing import Dict

from idact.core.config import RetryConfig
from idact.core.retry import Retry
from idact.detail.config.client.retry_config_impl import RetryConfigImpl


def serialize_retries(retries: Dict[Retry, RetryConfig]) -> dict:
    """Serializes retries to json.

        :param retries: Retries as config entry.

    """
    return {key.name: {'count': val.count,
                       'secondsBetween': val.seconds_between}
            for key, val in retries.items()}


def deserialize_retries(retries: dict) -> Dict[Retry, RetryConfig]:
    """Deserializes retries from json.

        :param retries: Retries as json.

    """
    return {Retry[key]: RetryConfigImpl(count=val['count'],
                                        seconds_between=val['secondsBetween'])
            for key, val in retries.items() if key in Retry.__members__}
