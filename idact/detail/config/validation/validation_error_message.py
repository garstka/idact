from typing import Optional


def validation_error_message(label: str,
                             value,
                             expected: Optional[str] = None,
                             regex: Optional[str] = None) -> str:
    """Formats a message for validation error.

        :param label:    The invalid item name.

        :param value:    The invalid item value.

        :param expected: The expected value. Default: no value provided.

        :param regex:    Expected value regex. Default: no regex provided.
    """
    return ("Invalid {label}: '{value}'.{optional_expected}"
            "{optional_regex}").format(label=label,
                                       value=value,
                                       optional_expected=(
                                           " Expected: {}".format(expected)
                                           if expected is not None else ''),
                                       optional_regex=(
                                           " Regex: r\"{}\".".format(regex)
                                           if regex is not None else ''))
