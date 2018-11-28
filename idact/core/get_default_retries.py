from typing import Dict

from idact.core.config import RetryConfig
from idact.core.retry import Retry
from idact.core.set_retry import set_retry


def get_default_retries() -> Dict[Retry, RetryConfig]:
    """Returns all default retry values."""
    return {
        Retry.PORT_INFO: set_retry(count=25, seconds_between=1),
        Retry.JUPYTER_JSON: set_retry(count=15, seconds_between=1),
        Retry.SCHEDULER_CONNECT: set_retry(count=5, seconds_between=2),
        Retry.DASK_NODE_CONNECT: set_retry(count=3, seconds_between=5),
        Retry.DEPLOY_DASK_SCHEDULER: set_retry(count=3, seconds_between=5),
        Retry.DEPLOY_DASK_WORKER: set_retry(count=3, seconds_between=5),
        Retry.GET_SCHEDULER_ADDRESS: set_retry(count=25, seconds_between=1),
        Retry.CHECK_WORKER_STARTED: set_retry(count=25, seconds_between=1),
        Retry.CANCEL_DEPLOYMENT: set_retry(count=5, seconds_between=1),
        Retry.SQUEUE_AFTER_SBATCH: set_retry(count=9, seconds_between=1),
        Retry.OPEN_TUNNEL: set_retry(count=3, seconds_between=5),
        Retry.VALIDATE_HTTP_TUNNEL: set_retry(count=6, seconds_between=1),
        Retry.TUNNEL_TRY_AGAIN_WITH_ANY_PORT: set_retry(count=1,
                                                        seconds_between=0)}
