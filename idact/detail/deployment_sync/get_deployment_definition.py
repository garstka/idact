from typing import Union

from idact.core.dask_deployment import DaskDeployment
from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.nodes import Nodes
from idact.detail.deployment_sync.deployment_definition import \
    DeploymentDefinition
from idact.detail.deployment_sync.nodes.get_nodes_deployment_definition \
    import get_nodes_deployment_definition
from idact.detail.nodes.nodes_impl import NodesImpl


def get_deployment_definition(deployment: Union[Nodes,
                                                JupyterDeployment,
                                                DaskDeployment]) -> DeploymentDefinition:  # noqa, pylint: disable=line-too-long
    """Obtains a definition of the deployment, that can be materialized
        later.

        :param deployment: Deployment, which definition to get.

    """
    if isinstance(deployment, Nodes):
        assert isinstance(deployment, NodesImpl)
        return get_nodes_deployment_definition(deployment)

    raise NotImplementedError()
