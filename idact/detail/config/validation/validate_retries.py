"""This module contains a function for validating a retry count."""

from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_RETRIES_DESCRIPTION = "Non-negative int."


def validate_retries(retries, label: str) -> int:
    """Returns the parameter if it's a valid retry count, otherwise raises
        an exception.

        Valid port is a non-negative integer.

        :param retries: Object to validate.

        :param label: Object label for error message.

        :raises TypeError: On wrong type.

        :raises ValueError: When integer is out of range.

    """
    if not isinstance(retries, int):
        raise TypeError(validation_error_message(
            label=label,
            value=retries,
            expected=VALID_RETRIES_DESCRIPTION))

    if retries < 0:
        raise ValueError(validation_error_message(
            label=label,
            value=retries,
            expected=VALID_RETRIES_DESCRIPTION))

    return retries
