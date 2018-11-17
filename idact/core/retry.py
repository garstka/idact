from enum import Enum


class Retry(Enum):
    """Retry action names."""

    PORT_INFO = 0
    """Fetch port info after deployment from a dir on NFS."""

    JUPYTER_JSON = 1
    """Fetch Jupyter nbserver.json from a dir on NFS."""

    SCHEDULER_CONNECT = 2
    """Connect to Dask scheduler from a node after Dask deployment."""

    DASK_NODE_CONNECT = 3
    """Connect to node before deploying Dask."""

    DEPLOY_DASK_SCHEDULER = 4
    """Deploy Dask scheduler."""

    DEPLOY_DASK_WORKER = 5
    """Deploy Dask worker."""

    GET_SCHEDULER_ADDRESS = 6
    """Obtain scheduler address from log."""

    CHECK_WORKER_STARTED = 7
    """Check worker started by analyzing the log."""

    CANCEL_DEPLOYMENT = 8
    """Kill the process tree of a deployment."""

    SQUEUE_AFTER_SBATCH = 9
    """Get info about the job just allocated with sbatch."""

    OPEN_TUNNEL = 10
    """Open ssh tunnel to node."""

    VALIDATE_HTTP_TUNNEL = 11
    """Connect to an HTTP server behind an ssh tunnel."""

    TUNNEL_TRY_AGAIN_WITH_ANY_PORT = 12
    """Fall back to any port if specific port tunnel fails."""
