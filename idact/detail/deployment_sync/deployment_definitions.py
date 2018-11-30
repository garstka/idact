from typing import Dict

from idact.detail.deployment_sync.deployment_definition import \
    DeploymentDefinition
from idact.detail.serialization.serializable import Serializable
from idact.detail.serialization.serializable_types import SerializableTypes


class DeploymentDefinitions(Serializable):
    """All synchronized deployment definitions.

        :param nodes: Allocation deployments.
        :param jupyter_deployments: Jupyter deployments.
        :param dask_deployments: Dask deployments.

    """

    def __init__(self,
                 nodes: Dict[str, DeploymentDefinition] = None,
                 jupyter_deployments: Dict[str, DeploymentDefinition] = None,
                 dask_deployments: Dict[str, DeploymentDefinition] = None):
        self._nodes = nodes if nodes is not None else {}
        self._jupyter_deployments = (jupyter_deployments
                                     if jupyter_deployments is not None
                                     else {})
        self._dask_deployments = (dask_deployments
                                  if dask_deployments is not None
                                  else {})

    @property
    def nodes(self) -> Dict[str, DeploymentDefinition]:
        """Allocation deployments by unique deployment id."""
        return self._nodes

    @property
    def jupyter_deployments(self) -> Dict[str, DeploymentDefinition]:
        """Jupyter deployments by unique deployment id."""
        return self._jupyter_deployments

    @property
    def dask_deployments(self) -> Dict[str, DeploymentDefinition]:
        """Dask deployments by unique deployment id."""
        return self._dask_deployments

    def serialize(self) -> dict:
        return {'type': str(SerializableTypes.DEPLOYMENT_DEFINITIONS),
                'nodes': {uuid: node.serialize()
                          for uuid, node in self._nodes.items()},
                'jupyter_deployments': {
                    uuid: jupyter.serialize()
                    for uuid, jupyter in self._jupyter_deployments.items()},
                'dask_deployments': {
                    uuid: dask.serialize()
                    for uuid, dask in self._dask_deployments.items()}}

    @staticmethod
    def deserialize(serialized: dict) -> 'DeploymentDefinitions':
        try:
            assert serialized['type'] == str(
                SerializableTypes.DEPLOYMENT_DEFINITIONS)
            nodes = {uuid: DeploymentDefinition.deserialize(serialized=node)
                     for uuid, node in serialized.get('nodes',
                                                      {}).items()}
            jupyter_deployments = {
                uuid: DeploymentDefinition.deserialize(serialized=node)
                for uuid, node in serialized.get('jupyter_deployments',
                                                 {}).items()}
            dask_deployments = {
                uuid: DeploymentDefinition.deserialize(serialized=node)
                for uuid, node in serialized.get('dask_deployments',
                                                 {}).items()}
            return DeploymentDefinitions(
                nodes=nodes,
                jupyter_deployments=jupyter_deployments,
                dask_deployments=dask_deployments)
        except KeyError as e:
            raise RuntimeError("Unable to deserialize.") from e

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
