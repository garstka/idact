from typing import List

import pytest

from idact import AuthMethod
from idact.core.retry import Retry
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.config.client.retry_config_impl import RetryConfigImpl
from idact.detail.helper.retry import retry, retry_with_config, \
    format_retry_failed_message


def failing_task(fail_times: int, failures: List[int]):
    """Fails fail_times, then returns 123.

        :param fail_times: Times to fail in a row before
                           success.

        :param failures: Empty list to append failure indices.

    """
    if fail_times <= len(failures):
        return 123

    if failures:
        failures.append(failures[-1] + 1)
    else:
        failures.append(0)
    raise RuntimeError()


def test_no_retries():
    failures = []
    with pytest.raises(RuntimeError):
        retry(fun=lambda: failing_task(fail_times=1, failures=failures),
              retries=0, seconds_between_retries=0)
    assert failures == [0]


def test_first_try_succeeds_no_retries():
    failures = []
    assert retry(fun=lambda: failing_task(fail_times=0, failures=failures),
                 retries=0, seconds_between_retries=0) == 123
    assert failures == []


def test_first_try_succeeds_one_retry():
    failures = []
    assert retry(fun=lambda: failing_task(fail_times=0, failures=failures),
                 retries=1, seconds_between_retries=0) == 123
    assert failures == []


def test_first_try_succeeds_some_retries():
    failures = []
    assert retry(fun=lambda: failing_task(fail_times=0, failures=failures),
                 retries=3, seconds_between_retries=0) == 123
    assert failures == []


def test_second_try_succeeds_no_retries():
    failures = []
    with pytest.raises(RuntimeError):
        retry(fun=lambda: failing_task(fail_times=1, failures=failures),
              retries=0, seconds_between_retries=0)
    assert failures == [0]


def test_second_try_succeeds_one_retry():
    failures = []
    assert retry(fun=lambda: failing_task(fail_times=1, failures=failures),
                 retries=1, seconds_between_retries=0) == 123
    assert failures == [0]


def test_second_try_succeeds_some_retries():
    failures = []
    assert retry(fun=lambda: failing_task(fail_times=1, failures=failures),
                 retries=3, seconds_between_retries=0) == 123
    assert failures == [0]


def test_third_try_succeeds_no_retries():
    failures = []
    with pytest.raises(RuntimeError):
        retry(fun=lambda: failing_task(fail_times=2, failures=failures),
              retries=0, seconds_between_retries=0)
    assert failures == [0]


def test_third_try_succeeds_one_retry():
    failures = []
    with pytest.raises(RuntimeError):
        retry(fun=lambda: failing_task(fail_times=2, failures=failures),
              retries=1, seconds_between_retries=0)
    assert failures == [0, 1]


def test_third_try_succeeds_some_retries():
    failures = []
    assert retry(fun=lambda: failing_task(fail_times=2, failures=failures),
                 retries=3, seconds_between_retries=0) == 123
    assert failures == [0, 1]


def test_third_try_succeeds_one_retry_with_config():
    failures = []
    config = ClusterConfigImpl(
        host='h', port=1, user='u', auth=AuthMethod.ASK,
        retries={Retry.PORT_INFO: RetryConfigImpl(
            count=1,
            seconds_between=0)})
    with pytest.raises(RuntimeError):
        retry_with_config(
            fun=lambda: failing_task(fail_times=2, failures=failures),
            name=Retry.PORT_INFO,
            config=config)
    assert failures == [0, 1]


def test_third_try_succeeds_some_retries_with_config():
    failures = []
    config = ClusterConfigImpl(
        host='h', port=1, user='u', auth=AuthMethod.ASK,
        retries={Retry.PORT_INFO: RetryConfigImpl(
            count=3,
            seconds_between=0)})
    assert retry_with_config(
        fun=lambda: failing_task(fail_times=2, failures=failures),
        name=Retry.PORT_INFO,
        config=config) == 123
    assert failures == [0, 1]


def test_retry_failed_message():
    formatted_message = format_retry_failed_message(name=Retry.PORT_INFO,
                                                    count=3,
                                                    seconds_between=5)
    assert formatted_message == (
        "Retried and failed: config.retries[Retry.PORT_INFO].{count=3, "
        "seconds_between=5}")
