from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_LOG_LEVEL_DESCRIPTION = 'An integer greater or equal to 0.'


def validate_log_level(log_level) -> int:
    """Valid log level is a positive integer.
       If the log level is invalid, raises a ValueError or TypeError.
       Otherwise, returns the log level

        :param log_level: Object to validate.
    """
    if not isinstance(log_level, int):
        raise TypeError(validation_error_message(
            label='log_level',
            value=log_level,
            expected=VALID_LOG_LEVEL_DESCRIPTION))

    if log_level < 0:
        raise ValueError(validation_error_message(
            label='log_level',
            value=log_level,
            expected=VALID_LOG_LEVEL_DESCRIPTION))

    return log_level
