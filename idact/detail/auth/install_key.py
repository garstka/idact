import logging
import os
from typing import Optional

from fabric.operations import run
import fabric.decorators
import fabric.tasks

from idact.core.auth import AuthMethod
from idact.detail.auth.generate_key import generate_key
from idact.detail.auth.get_public_key_location import get_public_key_location
from idact.detail.config.client.client_cluster_config \
    import ClientClusterConfig
from idact.detail.helper.raise_on_remote_fail import raise_on_remote_fail
from idact.detail.helper.yn_prompt import yn_prompt


def warn_if_not_public_key_auth(config: ClientClusterConfig,
                                log: logging.Logger):
    """Logs a warning, if the key is about to be installed,
       but public key authentication is off.

        :param config: Cluster config.

        :param log: Logger.

    """
    if config.auth != AuthMethod.PUBLIC_KEY:
        log.warning(
            "Installing key, despite"
            " auth method being {actual}"
            " instead of {expected}".format(
                actual=config.auth,
                expected=AuthMethod.PUBLIC_KEY))


def warn_if_install_flag_unset(config: ClientClusterConfig,
                               log: logging.Logger):
    """Logs a warning, if the key is about to be installed,
       but the install flag is off.

        :param config: Cluster config.

        :param log: Logger.

    """
    if not config.install_key:
        log.warning("Installing key, despite install key flag being unset.")


def try_getting_public_key_from_config(config: ClientClusterConfig,
                                       log: logging.Logger) -> Optional[str]:
    """Returns the public key path from config, or None, if a new pair
       should be generated.

        :param config: Cluster config.

        :param log: Logger.

    """

    if config.key is None:
        log.info("Private key not specified.")
        return None

    private_key_path = config.key
    private_key_found = os.path.isfile(private_key_path)
    if not private_key_found:
        log.error("Private key not found at: '{private_key_path}'".format(
            private_key_path=private_key_path))

    public_key_path = get_public_key_location(
        private_key_location=private_key_path)
    public_key_found = os.path.isfile(public_key_path)
    if not public_key_found:
        log.error("Public key not found at: '{public_key_path}'".format(
            public_key_path=public_key_path))

    if not private_key_found or not public_key_found:
        log.error("Unable to find specified public/private key pair.")
        if yn_prompt("Generate new public/private key pair?"):
            return None
        raise RuntimeError("Key pair missing, cannot install.")

    return public_key_path


def read_public_key(public_key_path: str) -> str:
    """Loads the public key from file or raises an error.

        :param public_key_path: Path to the public key.

    """
    with open(public_key_path, 'r') as file:
        public_key_lines = [i for i in file.readlines() if i]
        if len(public_key_lines) != 1:
            raise RuntimeError("Unexpected public key format"
                               " at '{public_key_path}':"
                               " Single line expected.")
        return public_key_lines[0]


def install_key(config: ClientClusterConfig):
    """Installs public key on access node.
       If it was not generated or it's missing, generates one.
       Expects password authentication to have already been performed.

        :param config: Cluster config for connection.

    """
    log = logging.getLogger(__name__)

    warn_if_not_public_key_auth(config=config, log=log)

    warn_if_install_flag_unset(config=config, log=log)

    public_key_path = try_getting_public_key_from_config(config=config,
                                                         log=log)

    if public_key_path is None:
        config.key = generate_key(host=config.host)
        public_key_path = get_public_key_location(
            private_key_location=config.key)

    public_key = read_public_key(public_key_path=public_key_path)

    @fabric.decorators.task
    def task():
        run("mkdir -p ~/.ssh")
        run("chmod 700 ~/.ssh")
        run("touch ~/.ssh/authorized_keys")
        run("chmod 644 ~/.ssh/authorized_keys")
        run("echo '{public_key}' >> ~/.ssh/authorized_keys".format(
            public_key=public_key))
        run("grep '{public_key}' ~/.ssh/authorized_keys".format(
            public_key=public_key))

    with raise_on_remote_fail(exception=RuntimeError):
        fabric.tasks.execute(task)
    config.install_key = False
