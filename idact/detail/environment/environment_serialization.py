"""This module contains functions for serializing and deserializing
    the environment."""

import json
import os
from typing import Optional

from idact.detail.config.client.client_config_serialize import \
    deserialize_client_config_from_json, serialize_client_config_to_json
from idact.detail.environment.environment import Environment
from idact.detail.environment.environment_impl import EnvironmentImpl

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

    data = serialize_client_config_to_json(environment.config)
    with open(path, 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)


def deserialize_environment_from_file(path: Optional[str] = None,
                                      ignore_if_missing: bool = False) -> Environment:  # noqa, pylint: disable=line-too-long
    """Loads the environment from file.

        See :func:`.load_environment`.

        :param path: Environment file path.
                     Default: IDACT_CONFIG_PATH environment variable,
                              or ~/.idact.conf

        :param ignore_if_missing: Do not raise :class:`.ValueError` if the file
                                  is missing. Default: `False`.

        :raises ValueError: On missing file if `ignore_if_missing` is not set
                            (default).

    """
    if path is None:
        path = os.environ.get('IDACT_CONFIG_PATH', DEFAULT_ENVIRONMENT_PATH)

    if not os.path.isfile(path):
        if ignore_if_missing:
            return EnvironmentImpl()
        else:
            raise ValueError("Not a valid environment file: {}".format(path))

    with open(path, 'r') as file:
        data = json.load(file)

    client_config = deserialize_client_config_from_json(data)
    return EnvironmentImpl(config=client_config)
