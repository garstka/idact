"""This module contains the implementation of the cluster config interface."""

from typing import Optional

from idact.core.auth import AuthMethod
from idact.core.config import ClusterConfig
from idact.detail.config.client.setup_actions_config import \
    SetupActionsConfigImpl
from idact.detail.config.validation.validate_hostname import validate_hostname
from idact.detail.config.validation.validate_bool import validate_bool
from idact.detail.config.validation.validate_key_path import validate_key_path
from idact.detail.config.validation.validate_port import validate_port
from idact.detail.config.validation.validate_scratch import validate_scratch
from idact.detail.config.validation.validate_setup_actions_config import \
    validate_setup_actions_config
from idact.detail.config.validation.validate_username import validate_username


class ClusterConfigImpl(ClusterConfig):
    """Client-side cluster config.

       For parameter description, see :class:`.ClusterConfig`.

       For defaults, see :func:`.add_cluster`.

    """

    def __init__(self,
                 host: str,
                 port: int,
                 user: str,
                 auth: AuthMethod,
                 key: Optional[str] = None,
                 install_key: bool = True,
                 disable_sshd: bool = False,
                 setup_actions: Optional[SetupActionsConfigImpl] = None,
                 scratch: Optional[str] = None):
        if install_key is None:
            install_key = True
        if disable_sshd is None:
            disable_sshd = False
        if setup_actions is None:
            setup_actions = SetupActionsConfigImpl()
        if scratch is None:
            scratch = '$HOME'

        self._host = validate_hostname(host)
        self._port = validate_port(port)
        self._user = validate_username(user)
        self._auth = auth
        self._key = validate_key_path(key)
        self._install_key = validate_bool(install_key, 'install_key')
        self._disable_sshd = validate_bool(disable_sshd, 'disable_sshd')
        self._setup_actions = validate_setup_actions_config(setup_actions)
        self._scratch = validate_scratch(scratch)

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = value

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value: int):
        self._port = value

    @property
    def user(self) -> str:
        return self._user

    @user.setter
    def user(self, value: str):
        self._user = value

    @property
    def auth(self) -> AuthMethod:
        return self._auth

    @auth.setter
    def auth(self, value: AuthMethod):
        self._auth = value

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

    @property
    def disable_sshd(self) -> bool:
        return self._disable_sshd

    @disable_sshd.setter
    def disable_sshd(self, value: bool):
        self._disable_sshd = value

    @property
    def setup_actions(self) -> SetupActionsConfigImpl:
        return self._setup_actions

    @property
    def scratch(self) -> str:
        return self._scratch

    @scratch.setter
    def scratch(self, value: str):
        self._scratch = value

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __str__(self):
        return ("({host},"
                " {port},"
                " {user},"
                " auth={auth},"
                " key={key},"
                " install_key={install_key},"
                " disable_sshd={disable_sshd})") \
            .format(host=self._host,
                    port=self._port,
                    user=self._user,
                    auth=self._auth,
                    key=repr(self._key),
                    install_key=self._install_key,
                    disable_sshd=self._disable_sshd)

    def __repr__(self):
        return str(self)
