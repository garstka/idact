from math import log2, ceil
from typing import Dict

from idact import get_default_retries, RetryConfig, Retry, set_retry
from tests.helpers.testing_environment import get_testing_process_count


def get_default_retries_heavy_load() -> Dict[Retry, RetryConfig]:
    """Multiplies each default retry count by the number of parallel testing
        processes. The testing container can come under heavy load when running
        tests in parallel, which sometimes results in timeouts."""
    testing_processes = get_testing_process_count()
    heavy_load_factor = (1.0 if testing_processes == 1
                         else log2(testing_processes))
    return {key: set_retry(count=int(ceil(config.count *
                                          testing_processes *
                                          heavy_load_factor)),
                           seconds_between=config.seconds_between)
            for key, config in get_default_retries().items()}
