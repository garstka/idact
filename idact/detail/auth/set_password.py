from contextlib import contextmanager


class PasswordCache:
    _password = None

    @property
    def password(self):
        return self._password


@contextmanager
def set_password(password: str):
    """Sets the host password in the context manager block.

        :param password: Password to use.
    """
    previous_password = PasswordCache().password
    PasswordCache._password = password  # pylint: disable=protected-access
    yield
    PasswordCache._password = previous_password  # noqa, pylint: disable=protected-access,line-too-long
