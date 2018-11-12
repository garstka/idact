from idact.core.get_default_retries import get_default_retries
from idact.detail.config.client.client_config_serialize \
    import serialize_retries

DEFAULT_RETRIES_JSON = serialize_retries(get_default_retries())
