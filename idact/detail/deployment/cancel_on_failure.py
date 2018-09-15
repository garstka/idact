"""This module contains a context manager for calling cancel on failure."""

from contextlib import contextmanager

from typing import Any


@contextmanager
def cancel_on_failure(obj: Any):
    """A context manager that calls cancel on the object, when an exception
        is thrown.

        :param obj: Object to execute cancel on.

    """
    try:
        yield
    except Exception as e:  # noqa, pylint: disable=broad-except
        obj.cancel()
        raise e
