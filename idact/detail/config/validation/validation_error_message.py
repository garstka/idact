from typing import Optional


def validation_error_message(label: str,
                             value,
                             expected: Optional[str] = None,
                             regex: Optional[str] = None) -> str:
    """Formats a message for validation error."""
    return ("Invalid {label}: '{value}'.{optional_expected}"
            "{optional_regex}").format(label=label,
                                       value=value,
                                       optional_expected=(
                                           " Expected: {}".format(expected)
                                           if expected is not None else ''),
                                       optional_regex=(
                                           " Regex: r\"{}\".".format(regex)
                                           if regex is not None else ''))
