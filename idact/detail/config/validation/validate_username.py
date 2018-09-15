"""This module contains a function for validating a username."""

import re

from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_USERNAME_REGEX = r"^.+$"
VALID_USERNAME_REGEX_DESCRIPTION = "One non-empty line."
__COMPILED = re.compile(pattern=VALID_USERNAME_REGEX)


def validate_username(username) -> str:
    """Returns the parameter, if it's a valid username, otherwise raises
        an exception

        A valid username is a string matching :attr:`.VALID_USERNAME_REGEX`.

        :param username: Object to validate.

        :raises ValueError: On regex mismatch.

    """
    if not __COMPILED.match(username):
        raise ValueError(validation_error_message(
            label='username',
            value=username,
            expected=VALID_USERNAME_REGEX_DESCRIPTION,
            regex=VALID_USERNAME_REGEX))
    return username
