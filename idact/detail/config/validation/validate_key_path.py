"""This module contains a function for validating a key path config entry."""

from typing import Optional

from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_PATH_DESCRIPTION = 'Non-empty string.'


def validate_key_path(path) -> Optional[str]:
    """Returns the parameter if it's a valid key path config entry, otherwise
        raises an exception.

        Key path is optional, non-empty string.

        :param path: Object to validate.

        :raises TypeError: On wrong type.

        :raises ValueError: On empty string.

    """
    if path is None:
        return path

    if not isinstance(path, str):
        raise TypeError(validation_error_message(
            label='path',
            value=path,
            expected=VALID_PATH_DESCRIPTION))

    if not path:
        raise ValueError(validation_error_message(
            label='path',
            value=path,
            expected=VALID_PATH_DESCRIPTION))

    return path
