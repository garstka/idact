import json

from idact.detail.config.client.client_config_serialize import \
    serialize_client_config_to_json, deserialize_client_config_from_json
from idact.detail.environment.environment import Environment
from idact.detail.environment.environment_impl import EnvironmentImpl


def serialize_environment(environment: Environment) -> str:
    """Returns the environment as a string.

        :param environment: Environment to save.

    """
    data = serialize_client_config_to_json(environment.config)
    return json.dumps(data, indent=4, sort_keys=True)


def deserialize_environment(text: str) -> Environment:
    """Loads the environment from string.

        :param text: Environment description.

    """
    data = json.loads(text)
    client_config = deserialize_client_config_from_json(data)
    return EnvironmentImpl(config=client_config)
