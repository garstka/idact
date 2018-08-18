"""This module contains a context manager for calling cancel on exit."""

from contextlib import contextmanager

from typing import Any


@contextmanager
def cancel_on_exit(obj: Any):
    """A context manager that calls cancel on the object on context exit.

        :param obj: Object to execute cancel on.
    """
    try:
        yield
    finally:
        obj.cancel()
