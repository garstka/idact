import pytest

from idact.core.retry import Retry
from idact.detail.config.client.client_config_serialize import \
    serialize_retries, deserialize_retries
from idact.detail.config.client.retry_config_impl import RetryConfigImpl


def test_retry_config():
    with pytest.raises(ValueError):
        RetryConfigImpl(count=-1, seconds_between=2)
    with pytest.raises(ValueError):
        RetryConfigImpl(count=1, seconds_between=-1)

    config = RetryConfigImpl(count=1, seconds_between=2)

    assert config == RetryConfigImpl(count=1, seconds_between=2)
    assert str(config) == repr(config)


def test_serialize_deserialize_retry_config():
    before = {Retry.PORT_INFO: RetryConfigImpl(count=1, seconds_between=2),
              Retry.JUPYTER_JSON: RetryConfigImpl(count=3, seconds_between=4)}

    expected_after = {'PORT_INFO': {'count': 1,
                                    'secondsBetween': 2},
                      'JUPYTER_JSON': {'count': 3,
                                       'secondsBetween': 4}}

    after = serialize_retries(before)

    assert expected_after == after

    deserialized = deserialize_retries(after)

    assert before == deserialized
