from typing import Dict

from idact.detail.deployment_sync.deployment_definition import \
    DeploymentDefinition
from idact.detail.serialization.serializable import Serializable
from idact.detail.serialization.serializable_types import SerializableTypes


class DeploymentDefinitions(Serializable):
    """All synchronized deployment definitions.

        :param nodes: Allocation deployments.

    """

    def __init__(self,
                 nodes: Dict[str, DeploymentDefinition] = None):
        self._nodes = nodes if nodes is not None else {}

    @property
    def nodes(self) -> Dict[str, DeploymentDefinition]:
        """Allocation deployments by unique deployment id."""
        return self._nodes

    def serialize(self) -> dict:
        return {'type': str(SerializableTypes.DEPLOYMENT_DEFINITIONS),
                'nodes': {uuid: node.serialize()
                          for uuid, node in self._nodes.items()}}

    @staticmethod
    def deserialize(serialized: dict) -> 'DeploymentDefinitions':
        try:
            assert serialized['type'] == str(
                SerializableTypes.DEPLOYMENT_DEFINITIONS)
            nodes = {uuid: DeploymentDefinition.deserialize(serialized=node)
                     for uuid, node in serialized['nodes'].items()}
            return DeploymentDefinitions(nodes=nodes)
        except KeyError as e:
            raise RuntimeError("Unable to deserialize.") from e

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
