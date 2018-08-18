"""This module contains a context manager that closes an SSH tunnel on
    failure."""

from contextlib import contextmanager

from idact.core.tunnel import Tunnel


@contextmanager
def close_tunnel_on_failure(tunnel: Tunnel):
    """A context manager that closes the tunnel when an exception is thrown."""
    try:
        yield
    except Exception as e:  # noqa, pylint: disable=broad-except
        tunnel.close()
        raise e
