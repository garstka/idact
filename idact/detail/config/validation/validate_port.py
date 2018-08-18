"""This module contains a function for validating a port number."""

from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_PORT_RANGE = range(1, 2 ** 16)
VALID_PORT_RANGE_DESCRIPTION = 'An integer from 1 to 65535.'


def validate_port(port) -> int:
    """Returns the parameter if it's a valid port, otherwise raises
        an exception.

        Valid port is an integer in range(1, 2**16).

        :param port: Object to validate.

        :raises TypeError: On wrong type.

        :raises ValueError: When integer is out of range.

    """
    if not isinstance(port, int):
        raise TypeError(validation_error_message(
            label='port',
            value=port,
            expected=VALID_PORT_RANGE_DESCRIPTION))

    if port not in VALID_PORT_RANGE:
        raise ValueError(validation_error_message(
            label='port',
            value=port,
            expected=VALID_PORT_RANGE_DESCRIPTION))

    return port
