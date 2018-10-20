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
                 nodes: Dict[str, DeploymentDefinition] = None,
                 jupyter_deployments: Dict[str, DeploymentDefinition] = None):
        self._nodes = nodes if nodes is not None else {}
        self._jupyter_deployments = (jupyter_deployments
                                     if jupyter_deployments is not None
                                     else {})

    @property
    def nodes(self) -> Dict[str, DeploymentDefinition]:
        """Allocation deployments by unique deployment id."""
        return self._nodes

    @property
    def jupyter_deployments(self) -> Dict[str, DeploymentDefinition]:
        """Jupyter deployments by unique deployment id."""
        return self._jupyter_deployments

    def serialize(self) -> dict:
        return {'type': str(SerializableTypes.DEPLOYMENT_DEFINITIONS),
                'nodes': {uuid: node.serialize()
                          for uuid, node in self._nodes.items()},
                'jupyter_deployments': {
                    uuid: jupyter.serialize()
                    for uuid, jupyter in self._jupyter_deployments.items()}}

    @staticmethod
    def deserialize(serialized: dict) -> 'DeploymentDefinitions':
        try:
            assert serialized['type'] == str(
                SerializableTypes.DEPLOYMENT_DEFINITIONS)
            nodes = {uuid: DeploymentDefinition.deserialize(serialized=node)
                     for uuid, node in serialized['nodes'].items()}
            jupyter_deployments = {
                uuid: DeploymentDefinition.deserialize(serialized=node)
                for uuid, node in serialized['jupyter_deployments'].items()}
            return DeploymentDefinitions(
                nodes=nodes,
                jupyter_deployments=jupyter_deployments)
        except KeyError as e:
            raise RuntimeError("Unable to deserialize.") from e

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
