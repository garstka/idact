"""This module contains a context manager for setting the Fabric exception
    to throw on remote command failure."""

from contextlib import contextmanager

from fabric.state import env


@contextmanager
def raise_on_remote_fail(exception=RuntimeError):
    """Context manager that sets the exception for Fabric to raise when
        a remote command fails (returns a non-zero exit status).

        :param exception: Exception to throw.

    """

    previous = env.abort_exception
    env.abort_exception = exception
    yield
    env.abort_exception = previous
