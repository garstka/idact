import datetime

from idact.detail.helper.utc_from_str import utc_from_str
from idact.detail.serialization.serializable import Serializable
from idact.detail.serialization.serializable_types import SerializableTypes


class DeploymentDefinition(Serializable):
    """Deployment definition that can be materialized into a deployment."""

    def __init__(self,
                 value: dict,
                 expiration_date: datetime.datetime):
        self._value = value
        self._expiration_date = expiration_date

    @property
    def value(self) -> dict:
        """Serialized deployment."""
        return self._value

    @property
    def expiration_date(self) -> datetime.datetime:
        """UTC datetime after which the deployment should be discarded."""
        return self._expiration_date

    def serialize(self) -> dict:
        return {'type': str(SerializableTypes.DEPLOYMENT_DEFINITION),
                'value': self._value,
                'expiration_date': self._expiration_date.isoformat()}

    @staticmethod
    def deserialize(serialized: dict) -> 'DeploymentDefinition':
        try:
            assert serialized['type'] == str(
                SerializableTypes.DEPLOYMENT_DEFINITION)
            return DeploymentDefinition(value=serialized['value'],
                                        expiration_date=utc_from_str(
                                            serialized['expiration_date']))
        except KeyError as e:
            raise RuntimeError("Unable to deserialize.") from e

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
