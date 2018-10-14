from typing import Union

from idact.core.nodes import Nodes
from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.dask_deployment import DaskDeployment
from idact.detail.deployment_sync.get_deployment_definition \
    import get_deployment_definition
from idact.detail.deployment_sync.deployment_definitions import \
    DeploymentDefinitions
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.nodes_impl import NodesImpl


def add_deployment_definition(deployments: DeploymentDefinitions,
                              deployment: Union[Nodes,
                                                JupyterDeployment,
                                                DaskDeployment]):
    """Adds the deployment to the list of deployment definitions.
        Replaces the deployment with the same unique id, if it already exists.

        :param deployments: Deployment definitions to extend.

        :param deployment: Deployment to add.

    """

    deployment_definition = get_deployment_definition(deployment=deployment)
    if isinstance(deployment, NodesImpl):
        target = deployments.nodes
        uuid = deployment.uuid
    else:
        raise NotImplementedError()

    if uuid in target:
        log = get_logger(__name__)
        log.warning("Overwriting deployment definition: %s", uuid)

    target[uuid] = deployment_definition