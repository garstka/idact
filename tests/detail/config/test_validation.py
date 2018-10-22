import pytest

from idact.detail.config.client.setup_actions_config import \
    SetupActionsConfigImpl
from idact.detail.config.validation.validate_cluster_name import \
    validate_cluster_name
from idact.detail.config.validation.validate_hostname import validate_hostname
from idact.detail.config.validation.validate_bool import validate_bool
from idact.detail.config.validation.validate_key_path import validate_key_path
from idact.detail.config.validation.validate_log_level \
    import validate_log_level
from idact.detail.config.validation.validate_notebook_defaults import \
    validate_notebook_defaults
from idact.detail.config.validation.validate_port import validate_port
from idact.detail.config.validation.validate_retries import validate_retries
from idact.detail.config.validation.validate_scratch import validate_scratch
from idact.detail.config.validation.validate_setup_actions import \
    validate_setup_actions
from idact.detail.config.validation.validate_setup_actions_config import \
    validate_setup_actions_config
from idact.detail.config.validation.validate_username import validate_username
from idact.detail.config.validation.validation_error_message import \
    validation_error_message


def test_validation_message():
    assert validation_error_message(label='Label',
                                    value='Value') == "Invalid Label: 'Value'."

    assert validation_error_message(label='LLL',
                                    value='VVV',
                                    expected='EEE.') == ("Invalid LLL: 'VVV'. "
                                                         "Expected: EEE.")

    assert validation_error_message(label='LLL',
                                    value='VVV',
                                    expected='EEE.',
                                    regex=r'\s') == ("Invalid LLL: 'VVV'. "
                                                     "Expected: EEE. "
                                                     "Regex: r\"\\s\".")


def test_validate_cluster_name():
    assert validate_cluster_name('clustername') == 'clustername'
    assert validate_cluster_name('Cluster N@me') == 'Cluster N@me'
    with pytest.raises(TypeError):
        validate_cluster_name(None)
    with pytest.raises(TypeError):
        validate_cluster_name(12)
    with pytest.raises(ValueError):
        validate_cluster_name('')
    with pytest.raises(ValueError):
        validate_cluster_name(' ')
    with pytest.raises(ValueError):
        validate_cluster_name(' clustername')
    with pytest.raises(ValueError):
        validate_cluster_name('cluster\name')


def test_validate_hostname():
    assert validate_hostname('hostname') == 'hostname'
    assert validate_hostname('host.name') == 'host.name'
    assert validate_hostname('host-name') == 'host-name'
    assert validate_hostname('HostName') == 'HostName'
    with pytest.raises(TypeError):
        validate_hostname(None)
    with pytest.raises(TypeError):
        validate_hostname(12)
    with pytest.raises(ValueError):
        validate_hostname('')
    with pytest.raises(ValueError):
        validate_hostname(' ')
    with pytest.raises(ValueError):
        validate_hostname('user@host')
    with pytest.raises(ValueError):
        validate_hostname('host!name')
    with pytest.raises(ValueError):
        validate_hostname('host\name')
    with pytest.raises(ValueError):
        validate_hostname('host_name')
    with pytest.raises(ValueError):
        validate_hostname('hostname.')
    with pytest.raises(ValueError):
        validate_hostname('.hostname')
    with pytest.raises(ValueError):
        validate_hostname('host name')
    with pytest.raises(ValueError):
        validate_hostname('hostname ')
    with pytest.raises(ValueError):
        validate_hostname(' hostname ')


def test_validate_bool():
    assert validate_bool(value=True)
    assert not validate_bool(value=False)

    with pytest.raises(TypeError):
        validate_bool('True')
    with pytest.raises(TypeError):
        validate_bool(12)


def test_validate_key_path():
    assert validate_key_path('path') == 'path'
    assert validate_key_path('/dir/file') == '/dir/file'
    assert validate_key_path('/dir/') == '/dir/'  # not checked at this point

    with pytest.raises(ValueError):
        validate_key_path('')
    with pytest.raises(TypeError):
        validate_key_path(12)
    with pytest.raises(TypeError):
        validate_key_path(True)


def test_validate_log_level():
    assert validate_log_level(0) == 0
    assert validate_log_level(1) == 1
    assert validate_log_level(22) == 22
    with pytest.raises(TypeError):
        validate_log_level(None)
    with pytest.raises(TypeError):
        validate_log_level('1')
    with pytest.raises(ValueError):
        validate_log_level(-1)
    with pytest.raises(ValueError):
        validate_log_level(-10)


def test_validate_port():
    assert validate_port(1) == 1
    assert validate_port(22) == 22
    assert validate_port(2 ** 16 - 1) == 2 ** 16 - 1
    with pytest.raises(TypeError):
        validate_port(None)
    with pytest.raises(TypeError):
        validate_port('1')
    with pytest.raises(ValueError):
        validate_port(-1)
    with pytest.raises(ValueError):
        validate_port(0)
    with pytest.raises(ValueError):
        validate_port(2 ** 16)
    with pytest.raises(ValueError):
        validate_port(2 ** 17)


def test_validate_scratch():
    assert validate_scratch('/') == '/'
    assert validate_scratch('/dir') == '/dir'
    assert validate_scratch('/a/') == '/a/'
    assert validate_scratch('/a/b') == '/a/b'
    assert validate_scratch('/a/b c d/ e f ') == '/a/b c d/ e f '

    with pytest.raises(ValueError):
        validate_scratch('')
    with pytest.raises(ValueError):
        validate_scratch(' /dir')
    with pytest.raises(ValueError):
        validate_scratch('dir')

    assert validate_scratch('$HOME') == '$HOME'
    assert validate_scratch('$VAR') == '$VAR'
    assert validate_scratch('$var') == '$var'
    assert validate_scratch('$VAR1') == '$VAR1'
    assert validate_scratch('$var2') == '$var2'

    with pytest.raises(ValueError):
        validate_scratch(' $HOME')
    with pytest.raises(ValueError):
        validate_scratch('$HOME ')
    with pytest.raises(ValueError):
        validate_scratch(' $VAR')
    with pytest.raises(ValueError):
        validate_scratch('$')
    with pytest.raises(ValueError):
        validate_scratch('$1')
    with pytest.raises(ValueError):
        validate_scratch('$ VAR')
    with pytest.raises(ValueError):
        validate_scratch('$$VAR')
    with pytest.raises(ValueError):
        validate_scratch('$VAR VAR')
    with pytest.raises(ValueError):
        validate_scratch('$VAR_VAR')
    with pytest.raises(ValueError):
        validate_scratch('$VAR=VAR')

    with pytest.raises(TypeError):
        validate_scratch(12)
    with pytest.raises(TypeError):
        validate_scratch(True)


def test_validate_setup_actions():
    assert validate_setup_actions([]) == []
    assert validate_setup_actions(['a']) == ['a']
    assert validate_setup_actions(['a', 'b']) == ['a', 'b']
    with pytest.raises(TypeError):
        validate_setup_actions([None])
    with pytest.raises(TypeError):
        validate_setup_actions(['a', 'b', None])
    with pytest.raises(TypeError):
        validate_setup_actions([1])
    with pytest.raises(TypeError):
        validate_setup_actions([1, 'a'])
    with pytest.raises(TypeError):
        validate_setup_actions(['a', 'b', 1])
    with pytest.raises(TypeError):
        validate_setup_actions(None)
    with pytest.raises(TypeError):
        validate_setup_actions('a')
    with pytest.raises(TypeError):
        validate_setup_actions(1)


def test_validate_setup_actions_config():
    assert validate_setup_actions_config(
        SetupActionsConfigImpl()) == SetupActionsConfigImpl()
    assert validate_setup_actions_config(SetupActionsConfigImpl(
        jupyter=['echo a'])) == SetupActionsConfigImpl(jupyter=['echo a'])

    with pytest.raises(TypeError):
        validate_setup_actions_config(None)
    with pytest.raises(TypeError):
        validate_setup_actions_config(1)
    with pytest.raises(TypeError):
        validate_setup_actions_config('a')


def test_validate_notebook_defaults():
    assert validate_notebook_defaults(
        {'a': 1}) == {'a': 1}

    with pytest.raises(TypeError):
        validate_notebook_defaults([])
    with pytest.raises(TypeError):
        validate_notebook_defaults(None)
    with pytest.raises(TypeError):
        validate_notebook_defaults(1)
    with pytest.raises(TypeError):
        validate_notebook_defaults('a')


def test_validate_username():
    assert validate_username('user') == 'user'
    assert validate_username(' us e@r ') == ' us e@r '
    with pytest.raises(TypeError):
        validate_username(None)
    with pytest.raises(TypeError):
        validate_username(12)
    with pytest.raises(ValueError):
        validate_username('')
    with pytest.raises(ValueError):
        validate_username('us\ner')


def test_validate_retries():
    assert validate_retries(0, label='') == 0
    assert validate_retries(1, label='') == 1
    assert validate_retries(22, label='') == 22
    with pytest.raises(TypeError):
        validate_retries(None, label='')
    with pytest.raises(TypeError):
        validate_retries('1', label='')
    with pytest.raises(ValueError):
        validate_retries(-1, label='')
    with pytest.raises(ValueError):
        validate_retries(-10, label='')
