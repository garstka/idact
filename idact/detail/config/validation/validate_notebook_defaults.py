from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_NOTEBOOK_DEFAULTS_DESCRIPTION = 'a dict'


def validate_notebook_defaults(value):
    """Returns the parameter, if it's a dict, otherwise raises an exception.

        :param value: Object to validate.

        :raises TypeError: On wrong type.

    """

    if isinstance(value, dict):
        return value

    raise TypeError(validation_error_message(
        label='notebook_defaults',
        value=value,
        expected=VALID_NOTEBOOK_DEFAULTS_DESCRIPTION))
