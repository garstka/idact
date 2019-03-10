from typing import Dict

from idact import get_default_retries, RetryConfig, Retry, set_retry
from tests.helpers.testing_environment import get_testing_process_count


def get_default_retries_heavy_load() -> Dict[Retry, RetryConfig]:
    """Multiplies each default retry count by the number of parallel testing
        processes. The testing container can come under heavy load when running
        tests in parallel, which sometimes results in timeouts."""
    testing_processes = get_testing_process_count()
    return {key: set_retry(count=config.count * testing_processes,
                           seconds_between=config.seconds_between)
            for key, config in get_default_retries().items()}
