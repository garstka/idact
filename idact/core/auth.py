"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.AuthMethod`.
"""

from enum import Enum


class AuthMethod(Enum):
    """Cluster authentication methods."""
    ASK = 0
    """Ask for password every time it's needed."""
    PUBLIC_KEY = 1
    """Generate a private and public key pair, and install the public key."""


class KeyType(Enum):
    """Key type to generate automatically."""
    RSA = 0
