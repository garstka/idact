from contextlib import contextmanager

from fabric.state import env


@contextmanager
def raise_on_remote_fail(exception=RuntimeError):
    """Sets the exception for Fabric to throw when a remote command fails.

        :param exception: Exception to throw."""

    previous = env.abort_exception
    env.abort_exception = exception
    yield
    env.abort_exception = previous
