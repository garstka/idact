import datetime

import dateutil.tz
import pytest

from idact.detail.deployment_sync.deployment_definition import \
    DeploymentDefinition


def test_serialize_deserialize():
    value = DeploymentDefinition(
        value={'a': 1,
               'b': '2'},
        expiration_date=(
            datetime.datetime(2018, 11, 12, 13, 14).replace(
                tzinfo=dateutil.tz.tzutc())))
    serialized = value.serialize()
    assert serialized == {'type': 'SerializableTypes.DEPLOYMENT_DEFINITION',
                          'value': {'a': 1,
                                    'b': '2'},
                          'expiration_date': '2018-11-12T13:14:00+00:00'}

    deserialized = DeploymentDefinition.deserialize(serialized=serialized)
    assert deserialized == value


def test_invalid_serialized_type():
    serialized = {'type': 'SerializableTypes.DEPLOYMENT_DEFINITION2'}

    with pytest.raises(AssertionError):
        DeploymentDefinition.deserialize(serialized=serialized)


def test_missing_serialized_keys():
    serialized = {'type': 'SerializableTypes.DEPLOYMENT_DEFINITION'}

    with pytest.raises(RuntimeError):
        DeploymentDefinition.deserialize(serialized=serialized)
