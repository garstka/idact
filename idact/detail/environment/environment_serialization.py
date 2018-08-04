import json
import os
from typing import Optional

from idact.detail.config.client.client_config_serialize import \
    deserialize_client_config_from_json, serialize_client_config_to_json
from idact.detail.environment.environment import Environment

DEFAULT_ENVIRONMENT_PATH = os.path.expanduser('~/.idact.conf')


def serialize_environment_to_file(environment: Environment,
                                  path: Optional[str]):
    """Dumps the environment to file.

        See :func:`.save_environment`.

        :param environment: Environment to save.

        :param path:        Output file path. Default: `~/.idact.conf`.

    """
    if path is None:
        path = DEFAULT_ENVIRONMENT_PATH

    data = serialize_client_config_to_json(environment.config)
    with open(path, 'w') as file:
        json.dump(data, file, indent=4, sort_keys=True)


def deserialize_environment_from_file(path: Optional[str] = None,
                                      raise_if_missing: bool = False):
    """Loads the environment from file.

        See :func:`.load_environment`.

        :param path:             Environment file path. Default: ~/.idact.conf

        :param raise_if_missing: Raise :class:`.ValueError` if the file is
                                 missing. Default: `False`.

        :raises ValueError: On missing file if `raise_if_missing` is set.

    """
    if path is None:
        path = DEFAULT_ENVIRONMENT_PATH

    if not os.path.isfile(path):
        if raise_if_missing:
            raise ValueError("Not a valid environment file: {}".format(path))
        else:
            return Environment()

    with open(path, 'r') as file:
        data = json.load(file)

    client_config = deserialize_client_config_from_json(data)
    return Environment(config=client_config)
