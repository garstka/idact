"""This module contains the implementation of the Dask diagnostics interface.
"""

import webbrowser
from typing import List

from idact.core.tunnel import Tunnel
from idact.core.dask_deployment import DaskDiagnostics


class DaskDiagnosticsImpl(DaskDiagnostics):
    """Implementation of the diagnostics interface."""

    def __init__(self, tunnels: List[Tunnel]):
        self._addresses = [
            "http://localhost:{port}".format(port=tunnel.here)
            for tunnel in tunnels]

    @property
    def addresses(self) -> List[str]:
        return self._addresses

    def open_all(self):
        for address in self._addresses:
            webbrowser.open(address)
