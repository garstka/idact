"""This module contains a function for validating a boolean config entry."""

from typing import Optional

from idact.detail.config.validation.validation_error_message import \
    validation_error_message


def validate_bool(value, label: Optional[str] = None) -> bool:
    """Returns the parameter, if it's a :class:`bool`, otherwise raises
        an exception.

        :param value: Object to validate.

        :param label: Object label for error message.

        :raises TypeError: On wrong type.

    """
    if isinstance(value, bool):
        return value

    raise TypeError(validation_error_message(
        label=label,
        value=value))
