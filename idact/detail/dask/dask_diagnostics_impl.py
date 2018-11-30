"""This module contains the implementation of the Dask diagnostics interface.
"""

import webbrowser
from typing import List

from idact.core.tunnel import Tunnel
from idact.core.dask_deployment import DaskDiagnostics


class DaskDiagnosticsImpl(DaskDiagnostics):
    """Implementation of the diagnostics interface."""

    def __init__(self,
                 scheduler_tunnel: Tunnel,
                 worker_tunnels: List[Tunnel]):
        self._addresses = [
            "http://localhost:{port}/status".format(
                port=scheduler_tunnel.here)]

        self._addresses.extend(
            ["http://localhost:{port}/main".format(port=tunnel.here)
             for tunnel in worker_tunnels])

    @property
    def addresses(self) -> List[str]:
        return self._addresses

    def open_all(self):
        for address in self._addresses:
            webbrowser.open(address)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
