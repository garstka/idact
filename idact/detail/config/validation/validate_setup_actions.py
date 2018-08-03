from typing import Optional, List

from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_SETUP_ACTIONS_DESCRIPTION = 'List of strings.'


def validate_setup_actions(value, label: Optional[str] = None) -> List[str]:
    """Key path is optional, non-empty string.

        :param path: Object to validate.
    """

    if isinstance(value, list) and all([isinstance(i, str) for i in value]):
        return value

    raise TypeError(validation_error_message(
        label=label,
        value=value,
        expected=VALID_SETUP_ACTIONS_DESCRIPTION))
