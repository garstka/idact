"""This module contains functionality for adding a password to cache."""

from contextlib import contextmanager

from typing import Optional


class PasswordCache:
    """Caches the host password."""
    _password = None  # type: Optional[str]

    @property
    def password(self) -> Optional[str]:
        """Current cached password."""
        return self._password


@contextmanager
def set_password(password: str):
    """Context manager that sets the host password for the context manager
        block.

        :param password: Password to use.
    """
    previous_password = PasswordCache().password
    PasswordCache._password = password  # pylint: disable=protected-access
    try:
        yield
    finally:
        PasswordCache._password = previous_password  # noqa, pylint: disable=protected-access,line-too-long
