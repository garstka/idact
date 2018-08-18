"""This module contains a way to disable :func:`.getpass`, in order to prevent
    password-authentication attempts by lower level libraries."""

import getpass
from contextlib import contextmanager


class GetpassExecutedError(RuntimeError):
    """Exception raised when :func:`.getpass` is executed unexpectedly."""
    pass


def fake_getpass(*_):
    """Raises :class:`.GetpassExecutedError` when :func:`getpass.getpass`
        is called."""
    raise GetpassExecutedError("Authentication fail:"
                               " Unexpected call to getpass occurred.")


@contextmanager
def disable_getpass():
    """Context manager that disables :func:`.getpass` being unconditionally
        called by Fabric after authentication fails."""
    store = getpass.getpass
    getpass.getpass = fake_getpass
    try:
        yield
    finally:
        getpass.getpass = store
