import os
import sys
from contextlib import contextmanager
from io import StringIO


class FakeStdin(StringIO):
    """Replacement for stdin in tests.

        See :func:`.disable_pytest_stdin`.

    """

    def __init__(self):
        super().__init__('')

    def fileno(self) -> int:
        """Returns the file number for stdin, i.e. 0."""
        return 0


@contextmanager
def disable_pytest_stdin():
    """Context manager that replaces :attr:`sys.stdin` as a fix for Fabric
        requiring a real file to back :attr:`sys.stdin` on Linux.

        Fabric's approach clashes with the way `pytest` captures standard
        input.

    """
    store = sys.stdin
    if os.name != 'nt':
        sys.stdin = FakeStdin()
    try:
        yield
    finally:
        sys.stdin = store
