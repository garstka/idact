"""This module contains functions for installing the public key on a cluster.
"""

import logging
import os
from io import BytesIO
from typing import Optional

from fabric.operations import run, get
import fabric.decorators
import fabric.tasks

from idact.core.config import ClusterConfig
from idact.detail.auth.generate_key import generate_key
from idact.detail.auth.get_public_key_location import get_public_key_location
from idact.detail.helper.raise_on_remote_fail import raise_on_remote_fail
from idact.detail.helper.yn_prompt import yn_prompt
from idact.detail.log.get_logger import get_logger


def try_getting_public_key_from_config(config: ClusterConfig,
                                       log: logging.Logger) -> Optional[str]:
    """Returns the public key path from config, or `None`, if a new pair
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
    """Loads the public key from file or raises a `RuntimeError`.

        :param public_key_path: Path to the public key.

    """
    with open(public_key_path, 'r') as file:
        public_key_lines = [i for i in file.readlines() if i]
        if len(public_key_lines) != 1:
            raise RuntimeError("Unexpected public key format"
                               " at '{public_key_path}':"
                               " Single line expected.")
        return public_key_lines[0]


def install_key(config: ClusterConfig,
                authorized_keys: Optional[str] = None):
    """Installs the public key on the access node.

        If it was not generated or it's missing, generates one.
        Expects password authentication to have already been performed.

        :param config: Cluster config for connection.

        :param authorized_keys: Path to authorized_keys.
                                Default: `~/.ssh/authorized_keys`
    """
    log = get_logger(__name__)

    authorized_keys_path = (authorized_keys
                            if authorized_keys
                            else ".ssh/authorized_keys")

    public_key_path = try_getting_public_key_from_config(config=config,
                                                         log=log)

    if public_key_path is None:
        config.key = generate_key(host=config.host)
        public_key_path = get_public_key_location(
            private_key_location=config.key)

    public_key = read_public_key(public_key_path=public_key_path)

    @fabric.decorators.task
    def task():
        """Creates the .ssh dir with proper permissions. Adds the public key
            to the authorized keys file if it's not been added already."""
        run("mkdir -p ~/.ssh")
        run("chmod 700 ~/.ssh")
        run("touch '{authorized_keys_path}'".format(
            authorized_keys_path=authorized_keys_path))
        run("chmod 644 '{authorized_keys_path}'".format(
            authorized_keys_path=authorized_keys_path))

        authorized_keys_fd = BytesIO()
        get(authorized_keys_path, authorized_keys_fd)
        authorized_keys_contents = \
            authorized_keys_fd.getvalue().decode('ascii').splitlines()

        if public_key not in authorized_keys_contents:
            run("echo '{public_key}' >> {authorized_keys_path}".format(
                public_key=public_key,
                authorized_keys_path=authorized_keys_path))
        run("grep '{public_key}' '{authorized_keys_path}'".format(
            public_key=public_key,
            authorized_keys_path=authorized_keys_path))

    with raise_on_remote_fail(exception=RuntimeError):
        fabric.tasks.execute(task)
