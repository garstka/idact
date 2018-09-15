import webbrowser
from contextlib import contextmanager

from typing import List


@contextmanager
def save_opened_in(result: List[str]):
    """Saves addresses opened by :func:`webbrowser.open`.

        :param result: List to append the addresses to.

    """

    addresses = []

    def fake_open(address: str):
        """Appends the opened address."""
        addresses.append(address)

    store = webbrowser.open
    webbrowser.open = fake_open
    try:
        yield
    finally:
        webbrowser.open = store
        result.extend(addresses)
