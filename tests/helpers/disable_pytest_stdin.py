import os
import sys
from contextlib import contextmanager
from io import StringIO


class FakeStdin(StringIO):
    def __init__(self):
        super().__init__('')

    def fileno(self):
        return 0


@contextmanager
def disable_pytest_stdin():
    """Fix for Fabric requiring a real file to back sys.stdin on Linux, which
       clashes with the way pytest captures stdin."""
    store = sys.stdin
    if os.name != 'nt':
        sys.stdin = FakeStdin()
    try:
        yield
    finally:
        sys.stdin = store
