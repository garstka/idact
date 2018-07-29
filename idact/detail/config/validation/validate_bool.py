from typing import Optional

from idact.detail.config.validation.validation_error_message import \
    validation_error_message


def validate_bool(value, label: Optional[str] = None) -> bool:
    """Validates a flag.

        :param value: Object to validate.
    """
    if isinstance(value, bool):
        return value

    raise TypeError(validation_error_message(
        label=label,
        value=value))
