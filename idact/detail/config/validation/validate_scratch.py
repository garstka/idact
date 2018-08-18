"""This module contains a function for validating a scratch config entry."""

import re

from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_SCRATCH_DESCRIPTION = 'Non-empty absolute path, or environment' \
                            ' variable name.'

VALID_SCRATCH_REGEX = r"^(/.*)|(\$[A-Za-z][A-Za-z0-9]*)$"  # noqa, pylint: disable=line-too-long

__COMPILED = re.compile(pattern=VALID_SCRATCH_REGEX)


def validate_scratch(scratch) -> str:
    """Returns the parameter if it's a valid scratch config entry, otherwise
        raises an exception.

        Key path is optional, non-empty string.

        :param scratch: Object to validate.

        :raises TypeError: On wrong type.

        :raises ValueError: On regex mismatch.

    """
    if not isinstance(scratch, str):
        raise TypeError(validation_error_message(
            label='scratch',
            value=scratch,
            expected=VALID_SCRATCH_DESCRIPTION,
            regex=VALID_SCRATCH_REGEX))

    if not __COMPILED.match(scratch):
        raise ValueError(validation_error_message(
            label='scratch',
            value=scratch,
            expected=VALID_SCRATCH_DESCRIPTION,
            regex=VALID_SCRATCH_REGEX))

    return scratch
