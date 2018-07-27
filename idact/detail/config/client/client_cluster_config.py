from typing import Optional

from idact.core.auth import AuthMethod
from idact.detail.config.validation.validate_hostname import validate_hostname
from idact.detail.config.validation.validate_install_key import \
    validate_install_key
from idact.detail.config.validation.validate_key_path import validate_key_path
from idact.detail.config.validation.validate_port import validate_port
from idact.detail.config.validation.validate_username import validate_username


class ClientClusterConfig:
    """Client-side cluster config.

       :param host: Cluster hostname.

       :param port: Cluster SSH port number.

       :param user: Cluster user to log in and run commands as.

       :param auth: Authentication method.

       :param key:         Private key path (if applicable).
                           It will be auto-generated if needed.

       :param install_key: True, if the key should be installed on cluster
                           before use.

    """

    def __init__(self,
                 host: str,
                 port: int,
                 user: str,
                 auth: AuthMethod,
                 key: Optional[str] = None,
                 install_key: bool = True):
        self._host = validate_hostname(host)
        self._port = validate_port(port)
        self._user = validate_username(user)
        self._auth = auth
        self._key = validate_key_path(key)
        self._install_key = validate_install_key(install_key)

    @property
    def host(self) -> str:
        return self._host

    @property
    def port(self) -> int:
        return self._port

    @property
    def user(self) -> str:
        return self._user

    @property
    def auth(self) -> AuthMethod:
        return self._auth

    @property
    def key(self) -> Optional[str]:
        return self._key

    @key.setter
    def key(self, value: Optional[str]):
        self._key = value

    @property
    def install_key(self) -> bool:
        return self._install_key

    @install_key.setter
    def install_key(self, value: bool):
        self._install_key = value

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return ("({host},"
                " {port},"
                " {user},"
                " auth={auth},"
                " key={key},"
                " install_key={install_key})") \
            .format(host=self._host,
                    port=self._port,
                    user=self._user,
                    auth=self._auth,
                    key=repr(self._key),
                    install_key=self._install_key)
