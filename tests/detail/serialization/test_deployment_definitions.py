import datetime

import dateutil.tz
import pytest

from idact.detail.deployment_sync.deployment_definitions import \
    DeploymentDefinitions
from idact.detail.deployment_sync.deployment_definition import \
    DeploymentDefinition


def test_serialize_deserialize():
    value = DeploymentDefinitions(
        nodes={
            '111': DeploymentDefinition(
                value={'a': 1,
                       'b': '2'},
                expiration_date=(
                    datetime.datetime(2018, 11, 12, 13, 14).replace(
                        tzinfo=dateutil.tz.tzutc()))),
            '222': DeploymentDefinition(
                value={'c': 3,
                       'd': '4'},
                expiration_date=(
                    datetime.datetime(2018, 11, 16, 17, 18).replace(
                        tzinfo=dateutil.tz.tzutc())))
        })
    serialized = value.serialize()
    assert serialized == {
        'type': 'SerializableTypes.DEPLOYMENT_DEFINITIONS',
        'nodes': {'111': {'type': 'SerializableTypes.DEPLOYMENT_DEFINITION',
                          'value': {'a': 1,
                                    'b': '2'},
                          'expiration_date': '2018-11-12T13:14:00+00:00'},
                  '222': {'type': 'SerializableTypes.DEPLOYMENT_DEFINITION',
                          'value': {'c': 3,
                                    'd': '4'},
                          'expiration_date': '2018-11-16T17:18:00+00:00'}}}

    deserialized = DeploymentDefinitions.deserialize(serialized=serialized)
    assert deserialized == value


def test_invalid_serialized_type():
    serialized = {'type': 'SerializableTypes.DEPLOYMENT_DEFINITIONS2'}

    with pytest.raises(AssertionError):
        DeploymentDefinitions.deserialize(serialized=serialized)


def test_missing_serialized_keys():
    serialized = {'type': 'SerializableTypes.DEPLOYMENT_DEFINITIONS'}

    with pytest.raises(RuntimeError):
        DeploymentDefinitions.deserialize(serialized=serialized)
