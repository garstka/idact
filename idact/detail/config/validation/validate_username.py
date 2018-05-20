import re

from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_USERNAME_REGEX = r"^.+$"
VALID_USERNAME_REGEX_DESCRIPTION = "One non-empty line."
__COMPILED = re.compile(pattern=VALID_USERNAME_REGEX)


def validate_username(username) -> str:
    """Valid username is a string matching VALID_USERNAME_REGEX.
       If username is invalid, raises a ValueError or TypeError.
       Otherwise, returns username."""
    if not __COMPILED.match(username):
        raise ValueError(validation_error_message(
            label='username',
            value=username,
            expected=VALID_USERNAME_REGEX_DESCRIPTION,
            regex=VALID_USERNAME_REGEX))
    return username
