import getpass
from contextlib import contextmanager


class GetpassExecutedError(RuntimeError):
    pass


def fake_getpass(*_):
    """Raises GetpassExecutedError when getpass.getpass is called."""
    raise GetpassExecutedError("Authentication fail:"
                               " Unexpected call to getpass occurred.")


@contextmanager
def disable_getpass():
    """Disables getpass being unconditionally called by Fabric after
       authentication fails."""
    store = getpass.getpass
    getpass.getpass = fake_getpass
    try:
        yield
    finally:
        getpass.getpass = store
