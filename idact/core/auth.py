"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.AuthMethod`, :class:`.KeyType`.
"""

from enum import Enum


class AuthMethod(Enum):
    """Cluster authentication methods.

        :attr:`.ASK`: Ask for password every time it's needed.

        :attr:`.PUBLIC_KEY`: Generate a private and public key pair, and
                             install the public key.

    """
    ASK = 0
    PUBLIC_KEY = 1


class KeyType(Enum):
    """Public key type."""
    RSA = 0
