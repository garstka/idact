from typing import Optional

from idact.detail.environment.environment_provider import EnvironmentProvider
from idact.detail.environment.environment_serialization import \
    serialize_environment_to_file, deserialize_environment_from_file


def load_environment(path: Optional[str] = None):
    """Loads the environment from file.

       :param path: Path to environment file. Default: ~/.idact.conf
    """
    environment = deserialize_environment_from_file(path=path)
    EnvironmentProvider().environment = environment


def save_environment(path: Optional[str] = None):
    """Saves the environment to file.

       :param path: Path to environment file. Default: ~/.idact.conf
    """
    environment = EnvironmentProvider().environment
    serialize_environment_to_file(environment=environment,
                                  path=path)
