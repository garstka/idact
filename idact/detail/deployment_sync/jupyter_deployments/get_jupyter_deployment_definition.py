from idact.detail.deployment_sync.deployment_definition import \
    DeploymentDefinition
from idact.detail.deployment_sync.nodes.get_expiration_date_from_nodes import \
    get_expiration_date_from_nodes
from idact.detail.jupyter.jupyter_deployment_impl import JupyterDeploymentImpl


# pylint: disable=bad-continuation
def get_jupyter_deployment_definition(
    jupyter_deployment: JupyterDeploymentImpl) -> DeploymentDefinition:  # noqa
    """Obtains a definition from a Jupyter deployment.
        Expiration date is the allocation end date of the node the notebook
        is deployed on, or one day from now if the node is not allocated.

        :param jupyter_deployment: Deployment to obtain the definition of.

    """

    expiration_date = get_expiration_date_from_nodes(
        nodes=[jupyter_deployment.deployment.node])
    return DeploymentDefinition(value=jupyter_deployment.serialize(),
                                expiration_date=expiration_date)
