from datetime import timedelta

from idact.detail.deployment_sync.deployment_definition import \
    DeploymentDefinition
from idact.detail.helper.utc_now import utc_now
from idact.detail.nodes.nodes_impl import NodesImpl


# pylint: disable=bad-continuation
def get_nodes_deployment_definition(
    deployment: NodesImpl) -> DeploymentDefinition:  # noqa
    """Obtains a definition from an allocation deployment.
        Expiration date is the minimum node allocation end date,
        or one day from now if the nodes were not yet allocated.

        :param deployment: Deployment to obtain the definition of.

    """

    expiration_dates = [node.allocated_until
                        for node in deployment
                        if node.allocated_until is not None]
    if expiration_dates:
        expiration_date = min(expiration_dates)
    else:
        expiration_date = utc_now() + timedelta(days=1)

    return DeploymentDefinition(value=deployment.serialize(),
                                expiration_date=expiration_date)
