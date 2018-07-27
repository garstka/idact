from contextlib import contextmanager


class PasswordCache:
    """Caches a host password."""
    _password = None

    @property
    def password(self):
        """Current cached password."""
        return self._password


@contextmanager
def set_password(password: str):
    """Sets the host password for the context manager block.

        :param password: Password to use.
    """
    previous_password = PasswordCache().password
    PasswordCache._password = password  # pylint: disable=protected-access
    try:
        yield
    finally:
        PasswordCache._password = previous_password  # noqa, pylint: disable=protected-access,line-too-long
