from typing import List

import pytest

from idact.detail.helper.retry import retry


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
