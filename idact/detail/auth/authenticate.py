from contextlib import contextmanager
from getpass import getpass

from fabric.state import env

from idact.core.auth import AuthMethod
from idact.detail.auth.set_password import PasswordCache
from idact.detail.config.client.client_cluster_config \
    import ClientClusterConfig


def get_host_string(user: str, host: str, port: int):
    """Returns a host string for Fabric."""
    return "{user}@{host}:{port}".format(user=user,
                                         host=host,
                                         port=port)


@contextmanager
def authenticate(host: str, config: ClientClusterConfig):
    if config.auth != AuthMethod.ASK:
        raise ValueError("Authentication method not implemented: '{}'.".format(
            config.auth))

    host_is_gateway = host == config.host

    gateway = get_host_string(user=config.user,
                              host=config.host,
                              port=config.port)

    previous_host = env.host_string
    previous_gateway = None

    if host_is_gateway:
        env.host_string = gateway
    else:
        previous_gateway = env.gateway
        env.gateway = gateway
        env.host_string = "{user}@{host}".format(user=config.user,
                                                 host=host)

    if PasswordCache().password is not None:
        env.password = PasswordCache().password
    else:
        env.password = getpass("Password for {user}@{host}: ".format(
            user=env.user,
            host=env.host))
    yield
    env.host_string = previous_host
    if not host_is_gateway:
        env.gateway = previous_gateway
    env.password = None
