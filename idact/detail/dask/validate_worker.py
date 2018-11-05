from idact.detail.dask.dask_worker_deployment import DaskWorkerDeployment
from idact.detail.tunnel.validate_tunnel_http_connection import \
    validate_tunnel_http_connection


def validate_worker(worker: DaskWorkerDeployment):
    """Validates the worker by accessing the diagnostics server.

        :param worker: Worker to validate.

    """
    validate_tunnel_http_connection(tunnel=worker.bokeh_tunnel)
