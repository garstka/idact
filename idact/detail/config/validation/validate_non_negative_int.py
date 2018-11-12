"""This module contains a function for validating a non-negative int."""

from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_NON_NEGATIVE_INT = "Non-negative int."


def validate_non_negative_int(value, label: str) -> int:
    """Returns the parameter if it's a non negative int, otherwise raises
        an exception.

        :param value: Object to validate.

        :param label: Object label for error message.

        :raises TypeError: On wrong type.

        :raises ValueError: When integer is out of range.

    """
    if not isinstance(value, int):
        raise TypeError(validation_error_message(
            label=label,
            value=value,
            expected=VALID_NON_NEGATIVE_INT))

    if value < 0:
        raise ValueError(validation_error_message(
            label=label,
            value=value,
            expected=VALID_NON_NEGATIVE_INT))

    return value
