"""This module contains the implementation of the cluster config interface."""

from typing import Optional, Dict

from idact.core.auth import AuthMethod
from idact.core.config import ClusterConfig, RetryConfig
from idact.core.retry import Retry
from idact.detail.config.client.setup_actions_config import \
    SetupActionsConfigImpl
from idact.detail.config.defaults.provide_defaults_for_retries import \
    provide_defaults_for_retries
from idact.detail.config.validation.validate_hostname import validate_hostname
from idact.detail.config.validation.validate_bool import validate_bool
from idact.detail.config.validation.validate_key_path import validate_key_path
from idact.detail.config.validation.validate_notebook_defaults import \
    validate_notebook_defaults
from idact.detail.config.validation.validate_port import validate_port
from idact.detail.config.validation.validate_retry_config_dict import \
    validate_retry_config_dict
from idact.detail.config.validation.validate_scratch import validate_scratch
from idact.detail.config.validation.validate_setup_actions_config import \
    validate_setup_actions_config
from idact.detail.config.validation.validate_username import validate_username


class ClusterConfigImpl(ClusterConfig):
    """Client-side cluster config.

        For parameter description, see :class:`.ClusterConfig`.

        For defaults, see :func:`.add_cluster`.

        For notebook defaults, see :mod:`.jupyter_app.main`

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
                 scratch: Optional[str] = None,
                 notebook_defaults: Optional[dict] = None,
                 retries: Optional[Dict[Retry, RetryConfig]] = None,
                 use_jupyter_lab: bool = True):
        if install_key is None:
            install_key = True
        if disable_sshd is None:
            disable_sshd = False
        if setup_actions is None:
            setup_actions = SetupActionsConfigImpl()
        if scratch is None:
            scratch = '$HOME'
        if notebook_defaults is None:
            notebook_defaults = {}
        if retries is None:
            retries = {}
        if use_jupyter_lab is None:
            use_jupyter_lab = True

        retries = provide_defaults_for_retries(retries)

        self._host = None
        self.host = host

        self._port = None
        self.port = port

        self._user = None
        self.user = user

        self._auth = None
        self.auth = auth

        self._key = None
        self.key = key

        self._install_key = None
        self.install_key = install_key

        self._disable_sshd = None
        self.disable_sshd = disable_sshd

        self._setup_actions = validate_setup_actions_config(setup_actions)

        self._scratch = None
        self.scratch = scratch

        self._notebook_defaults = None
        self.notebook_defaults = notebook_defaults

        self._retries = validate_retry_config_dict(retries, 'retries')

        self._use_jupyter_lab = None
        self.use_jupyter_lab = use_jupyter_lab

    @property
    def host(self) -> str:
        return self._host

    @host.setter
    def host(self, value: str):
        self._host = validate_hostname(value)

    @property
    def port(self) -> int:
        return self._port

    @port.setter
    def port(self, value: int):
        self._port = validate_port(value)

    @property
    def user(self) -> str:
        return self._user

    @user.setter
    def user(self, value: str):
        self._user = validate_username(value)

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
        self._key = validate_key_path(value)

    @property
    def install_key(self) -> bool:
        return self._install_key

    @install_key.setter
    def install_key(self, value: bool):
        self._install_key = validate_bool(value, 'install_key')

    @property
    def disable_sshd(self) -> bool:
        return self._disable_sshd

    @disable_sshd.setter
    def disable_sshd(self, value: bool):
        self._disable_sshd = validate_bool(value, 'disable_sshd')

    @property
    def setup_actions(self) -> SetupActionsConfigImpl:
        return self._setup_actions

    @property
    def scratch(self) -> str:
        return self._scratch

    @scratch.setter
    def scratch(self, value: str):
        self._scratch = validate_scratch(value)

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

    @property
    def notebook_defaults(self) -> dict:
        """Defaults for the notebook app."""
        return self._notebook_defaults

    @notebook_defaults.setter
    def notebook_defaults(self, value: dict):
        self._notebook_defaults = validate_notebook_defaults(value)

    @property
    def retries(self) -> Dict[Retry, RetryConfig]:
        return self._retries

    @property
    def use_jupyter_lab(self) -> bool:
        return self._use_jupyter_lab

    @use_jupyter_lab.setter
    def use_jupyter_lab(self, value: bool):
        self._use_jupyter_lab = validate_bool(value, 'use_jupyter_lab')
