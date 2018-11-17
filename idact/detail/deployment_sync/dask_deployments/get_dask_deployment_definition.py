# pylint: disable=bad-continuation
from idact.detail.dask.dask_deployment_impl import DaskDeploymentImpl
from idact.detail.deployment_sync.deployment_definition import \
    DeploymentDefinition
from idact.detail.deployment_sync.nodes.get_expiration_date_from_nodes import \
    get_expiration_date_from_nodes


def get_dask_deployment_definition(
    dask_deployment: DaskDeploymentImpl) -> DeploymentDefinition:  # noqa
    """Obtains a definition from a Dask deployment.
        Expiration date is the minimum allocation end date of the node
        the scheduler is deployed on, or one day from now if the node
        is not allocated.

        :param dask_deployment: Deployment to obtain the definition of.

    """

    expiration_date = get_expiration_date_from_nodes(
        nodes=[dask_deployment.scheduler.deployment.node])
    return DeploymentDefinition(value=dask_deployment.serialize(),
                                expiration_date=expiration_date)
