"""This module contains a function for validating a setup actions list."""

from typing import Optional, List

from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_SETUP_ACTIONS_DESCRIPTION = 'List of strings.'


def validate_setup_actions(value, label: Optional[str] = None) -> List[str]:
    """Returns the parameter, if it's a valid setup actions entry, otherwise
        raises an exception.

        A valid setup actions entry is a list of strings.

        :param value: Object to validate.

        :param label: Object label for error message.

        :raises TypeError: On wrong type.

    """

    if isinstance(value, list) and all([isinstance(i, str) for i in value]):
        return value

    raise TypeError(validation_error_message(
        label=label,
        value=value,
        expected=VALID_SETUP_ACTIONS_DESCRIPTION))
