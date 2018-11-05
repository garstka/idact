from idact.detail.deployment_sync.deployment_definition import \
    DeploymentDefinition
from idact.detail.deployment_sync.nodes.get_expiration_date_from_nodes \
    import get_expiration_date_from_nodes
from idact.detail.nodes.nodes_impl import NodesImpl


# pylint: disable=bad-continuation
def get_nodes_deployment_definition(
    deployment: NodesImpl) -> DeploymentDefinition:  # noqa
    """Obtains a definition from an allocation deployment.
        Expiration date is the minimum node allocation end date,
        or one day from now if the nodes were not yet allocated.

        :param deployment: Deployment to obtain the definition of.

    """

    expiration_date = get_expiration_date_from_nodes(nodes=deployment)
    return DeploymentDefinition(value=deployment.serialize(),
                                expiration_date=expiration_date)
