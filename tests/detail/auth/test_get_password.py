import getpass

from idact import AuthMethod
from idact.detail.auth.get_password import get_password
from idact.detail.auth.set_password import PasswordCache
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl


def test_get_password():
    config = ClusterConfigImpl(
        host='host',
        port=1234,
        user='user',
        auth=AuthMethod.ASK)

    PasswordCache()._password = None  # pylint: disable=protected-access

    output = []

    def fake_getpass(prompt: str) -> str:
        output.append(prompt)
        return 'fakepass'

    saved_getpass = None
    try:
        saved_getpass = getpass.getpass
        getpass.getpass = fake_getpass
        assert get_password(config) == 'fakepass'
        assert output == ["Password for user@host:1234: "]
    finally:
        if saved_getpass is not None:
            getpass.getpass = saved_getpass
