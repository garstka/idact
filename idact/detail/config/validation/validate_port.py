from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_PORT_RANGE = range(1, 2 ** 16)
VALID_PORT_RANGE_DESCRIPTION = 'An integer from 1 to 65535.'


def validate_port(port) -> int:
    """Valid port is an integer in range(1, 2**16)
       If port is invalid, raises a ValueError or TypeError.
       Otherwise, returns port.

        :param port: Object to validate.
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
