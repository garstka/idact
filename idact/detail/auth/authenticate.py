from contextlib import contextmanager

from fabric.state import env

from idact.core.auth import AuthMethod
from idact.detail.auth.get_host_string import get_host_string
from idact.detail.auth.get_password import get_password
from idact.detail.config.client.client_cluster_config \
    import ClientClusterConfig


@contextmanager
def authenticate(host: str, config: ClientClusterConfig):
    """Authenticates the user in Fabric.

        :param host: SSH host.

        :param config: Cluster config.
    """
    if config.auth != AuthMethod.ASK:
        raise ValueError("Authentication method not implemented: '{}'.".format(
            config.auth))

    host_is_gateway = host == config.host

    gateway = get_host_string(config=config)

    previous_host = env.host_string
    previous_gateway = None

    if host_is_gateway:
        env.gateway = None
        env.host_string = gateway
    else:
        previous_gateway = env.gateway
        env.gateway = gateway
        env.host_string = "{user}@{host}".format(user=config.user,
                                                 host=host)

    env.password = get_password(config=config)
    yield
    env.host_string = previous_host
    if not host_is_gateway:
        env.gateway = previous_gateway
    env.password = None
