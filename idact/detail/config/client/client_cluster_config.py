from idact.core.auth import AuthMethod
from idact.detail.config.validation.validate_hostname import validate_hostname
from idact.detail.config.validation.validate_port import validate_port
from idact.detail.config.validation.validate_username import validate_username


class ClientClusterConfig:
    """Client-side cluster config.

       :param host: Cluster hostname.

       :param port: Cluster SSH port number.

       :param user: Cluster user to log in and run commands as.

       :param auth: Authentication method.
    """

    def __init__(self,
                 host: str,
                 port: int,
                 user: str,
                 auth: AuthMethod):
        self._host = validate_hostname(host)
        self._port = validate_port(port)
        self._user = validate_username(user)
        self._auth = auth

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

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return "({host}, {port}, {user}, {auth})".format(host=self._host,
                                                         port=self._port,
                                                         user=self._user,
                                                         auth=self._auth)
