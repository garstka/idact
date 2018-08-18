"""This module contains a function for determining the public key location
    from private key path."""


def get_public_key_location(private_key_location: str) -> str:
    """Returns the location of the public key based on the location of
        the private key.

        :param private_key_location: Private key location.

    """
    return private_key_location + ".pub"
