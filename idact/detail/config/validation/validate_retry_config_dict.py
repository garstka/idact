"""This module contains a function for validating a retry config dict.
"""
from typing import Dict

from idact.core.config import RetryConfig
from idact.core.retry import Retry
from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_RETRY_CONFIG_DICT_DESCRIPTION = (
    'Dict of with Retry enum keys and RetryConfig values (see set_retry).')


def validate_retry_config_dict(value, label: str) -> Dict[Retry, RetryConfig]:
    """Returns the parameter, if it's dict of with :class:`.Retry` keys and
        :class:`.RetryConfig' values.

        :param value: Object to validate.

        :param label: Error message label.

        :raises TypeError: On wrong type.

    """

    if isinstance(value, dict) and all([isinstance(key, Retry) and
                                        isinstance(val, RetryConfig)
                                        for key, val in value.items()]):
        return value

    raise TypeError(validation_error_message(
        label=label,
        value=value,
        expected=VALID_RETRY_CONFIG_DICT_DESCRIPTION))
