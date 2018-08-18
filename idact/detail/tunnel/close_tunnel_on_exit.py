"""This module contains a context manager that closes an SSH tunnel on exit."""

from contextlib import contextmanager

from idact.core.tunnel import Tunnel


@contextmanager
def close_tunnel_on_exit(tunnel: Tunnel):
    """A context manager that closes the tunnel on context exit."""
    try:
        yield
    finally:
        tunnel.close()
