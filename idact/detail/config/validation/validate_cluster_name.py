"""This module contains a function for validating a cluster name."""

import re
from idact.detail.config.validation.validation_error_message import \
    validation_error_message

# Based on regex by Martijn Pieters
# https://stackoverflow.com/questions/15954650/python-how-do-i-use-re-to-match-a-whole-string

VALID_CLUSTER_NAME_REGEX = r"^(?!\s)^.+(?<!\s)$"
VALID_CLUSTER_NAME_REGEX_DESCRIPTION = (
    "One line with at least one character and no leading or trailing space.")
__COMPILED = re.compile(pattern=VALID_CLUSTER_NAME_REGEX)


def validate_cluster_name(cluster_name) -> str:
    """Returns the parameter if it's a valid cluster name,
        otherwise raises an exception.

        Valid cluster name is a string matching
        :attr:`.VALID_CLUSTER_NAME_REGEX`.

        :param cluster_name: Object to validate.

        :raises ValueError: On regex mismatch.

    """
    if not __COMPILED.match(cluster_name):
        raise ValueError(validation_error_message(
            label='cluster name',
            value=cluster_name,
            expected=VALID_CLUSTER_NAME_REGEX_DESCRIPTION,
            regex=VALID_CLUSTER_NAME_REGEX))

    return cluster_name
