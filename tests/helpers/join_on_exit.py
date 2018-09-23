from contextlib import contextmanager
from threading import Thread


@contextmanager
def join_on_exit(thread: Thread):
    """A context manager that joins the thread on context exit."""
    try:
        yield
    finally:
        thread.join()
