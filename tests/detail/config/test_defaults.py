from idact.core.get_default_retries import get_default_retries
from idact.core.retry import Retry
from idact.detail.config.client.retry_config_impl import RetryConfigImpl
from idact.detail.config.defaults.provide_defaults_for_retries import \
    provide_defaults_for_retries


def test_defaults_for_retries():
    assert provide_defaults_for_retries({}) == get_default_retries()


def test_defaults_do_not_override_existing_values():
    with_defaults = provide_defaults_for_retries(
        {Retry.JUPYTER_JSON: RetryConfigImpl(
            count=0,
            seconds_between=0)})
    assert with_defaults[Retry.JUPYTER_JSON] == RetryConfigImpl(
        count=0,
        seconds_between=0)
