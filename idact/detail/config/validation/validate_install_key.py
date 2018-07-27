from idact.detail.config.validation.validation_error_message import \
    validation_error_message


def validate_install_key(install_key) -> bool:
    """Install key flag.

        :param install_key: Object to validate.
    """
    if isinstance(install_key, bool):
        return install_key

    raise TypeError(validation_error_message(
        label='install_key',
        value=install_key))
