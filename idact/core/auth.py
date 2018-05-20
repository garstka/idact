from enum import Enum


class AuthMethod(Enum):
    """Cluster authentication methods."""
    ASK = 0
    """Ask for password every time it's needed."""
