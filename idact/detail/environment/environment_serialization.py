"""This module contains functions for serializing and deserializing
    the environment."""

import os
from typing import Optional

from idact.detail.environment.environment import Environment
from idact.detail.environment.environment_text_serialization import \
    serialize_environment, deserialize_environment

DEFAULT_ENVIRONMENT_PATH = os.path.expanduser('~/.idact.conf')


def serialize_environment_to_file(environment: Environment,
                                  path: Optional[str]):
    """Dumps the environment to file.

        See :func:`.save_environment`.

        :param environment: Environment to save.

        :param path: Output file path.
                     Default: IDACT_CONFIG_PATH environment variable,
                     or ~/.idact.conf

    """
    if path is None:
        path = os.environ.get('IDACT_CONFIG_PATH', DEFAULT_ENVIRONMENT_PATH)

    text = serialize_environment(environment)
    with open(path, 'w') as file:
        file.write(text)


def deserialize_environment_from_file(path: Optional[str] = None) \
    -> Environment:  # noqa, pylint: disable=line-too-long
    """Loads the environment from file.

        See :func:`.load_environment`.

        :param path: Environment file path.
                     Default: IDACT_CONFIG_PATH environment variable,
                     or ~/.idact.conf

        :raises ValueError: On missing file if `ignore_if_missing` is not set
                            (default).

    """
    if path is None:
        path = os.environ.get('IDACT_CONFIG_PATH', DEFAULT_ENVIRONMENT_PATH)

    if not os.path.isfile(path):
        raise ValueError("Not a valid environment file: {}".format(path))

    with open(path, 'r') as file:
        file_contents = file.read()

    return deserialize_environment(text=file_contents)
