"""This module contains functionality for determining a free private key
    location."""

import os
import random
import string

from typing import Optional

from idact.core.auth import KeyType
from idact.detail.auth.get_public_key_location import get_public_key_location
from idact.detail.log.get_logger import get_logger

KEY_NAME_PREFIX = {KeyType.RSA: 'id_rsa_'}
KEY_NAME_SUFFIX_LENGTH = 2
KEY_NAME_SUFFIX_RETRIES = 4
KEY_NAME_SUFFIX_MAX_LENGTH = 32


def get_key_suffix(length: int) -> str:
    """Returns a pseudo-random lowercase string.

        :param length: Generated string length.

    """
    return ''.join(random.choice(string.ascii_lowercase + string.digits)
                   for _ in range(length))


def get_key_path(location: str,
                 prefix: str,
                 suffix: str):
    """Constructs the key path from components.

        :param location: Key directory.

        :param prefix: Key name prefix.

        :param suffix: Key name suffix.

    """
    return os.path.join(location, prefix + suffix)


def try_generate_unique_path(suffix_length: int,
                             location: str,
                             prefix: str) -> Optional[str]:
    """Tries to generate a unique file name.
        Returns None if the file already exists.

        :param suffix_length: File name suffix length.

        :param location: File parent dir.

        :param prefix: File name prefix.

    """
    log = get_logger(__name__)
    suffix = get_key_suffix(length=suffix_length)

    private_key_path = get_key_path(location=location,
                                    prefix=prefix,
                                    suffix=suffix)
    if os.path.isfile(private_key_path):
        log.warning("File exists: '%s'.", private_key_path)
        return None

    public_key_path = get_public_key_location(
        private_key_location=private_key_path)
    if os.path.isfile(public_key_path):
        log.warning("File exists: '%s'.", public_key_path)
        return None

    return private_key_path


def get_free_private_key_location(key_type: KeyType) -> str:
    """Returns a path for a new private key.

        The parent directory is determined by the environment variable
        `IDACT_KEY_LOCATION`. If it's not set, `~/.ssh` is used.

        :param key_type: Generated key type.

    """

    location = os.environ.get('IDACT_KEY_LOCATION',
                              default=os.path.expanduser('~/.ssh'))
    os.makedirs(location, exist_ok=True)

    prefix = KEY_NAME_PREFIX[key_type]

    key_path = None
    suffix_length = KEY_NAME_SUFFIX_LENGTH
    while suffix_length <= KEY_NAME_SUFFIX_MAX_LENGTH:
        for _ in range(0, KEY_NAME_SUFFIX_RETRIES):
            key_path = try_generate_unique_path(suffix_length=suffix_length,
                                                location=location,
                                                prefix=prefix)
            if key_path is not None:
                break
        if key_path is not None:
            break

        suffix_length *= 2

    if key_path is None:
        raise RuntimeError("Unable to generate unique key filename.")

    return key_path
