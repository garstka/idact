"""This module contains a function for generating SSH keys."""

import datetime

from paramiko import RSAKey

from idact.core.auth import KeyType
from idact.detail.auth.get_free_private_key_location import \
    get_free_private_key_location
from idact.detail.auth.get_public_key_location import get_public_key_location

RSA_BITS = 4096


def generate_key(host: str, key_type: KeyType = KeyType.RSA) -> str:
    """Generates a new private-public key pair and returns the path
        to the private key.

        Private key is saved in a directory determined by
        :func:`get_free_private_key_location`.

        :param host: Host name for identification purposes.

        :param key_type: Key type to generate.

    """
    if key_type != KeyType.RSA:
        raise NotImplementedError("Only RSA keys are supported for now.")

    key = RSAKey.generate(bits=RSA_BITS)

    private_key_location = get_free_private_key_location(key_type=key_type)
    key.write_private_key_file(filename=private_key_location)

    public_key = RSAKey(filename=private_key_location)

    now_down_to_minutes = datetime.datetime.now().isoformat()[:16]
    comment = "idact/{host}/{now_down_to_minutes}".format(
        host=host,
        now_down_to_minutes=now_down_to_minutes)

    public_key_value = "{name} {base64} {comment}".format(
        name=public_key.get_name(),
        base64=public_key.get_base64(),
        comment=comment)

    public_key_location = get_public_key_location(
        private_key_location=private_key_location)

    with open(public_key_location, 'w') as file:
        file.write(public_key_value)

    return private_key_location
