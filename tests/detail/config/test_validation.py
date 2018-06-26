import pytest

from idact.detail.config.validation.validate_cluster_name import \
    validate_cluster_name
from idact.detail.config.validation.validate_hostname import validate_hostname
from idact.detail.config.validation.validate_port import validate_port
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
