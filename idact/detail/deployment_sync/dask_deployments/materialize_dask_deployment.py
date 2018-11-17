from idact.core.config import ClusterConfig
from idact.detail.dask.dask_deployment_impl import DaskDeploymentImpl
from idact.detail.deployment_sync.deployment_definition import \
    DeploymentDefinition


# pylint: disable=bad-continuation
def materialize_dask_deployment(
    config: ClusterConfig,
    uuid: str,
    definition: DeploymentDefinition) -> DaskDeploymentImpl:  # noqa
    """Materializes the Dask deployment definition.

        :param config:      Cluster to materialize the deployment with.
        :param uuid:        Unique deployment id.
        :param definition:  Deployment definition to materialize.

    """
    deployment = DaskDeploymentImpl.deserialize(
        config=config,
        uuid=uuid,
        serialized=definition.value)
    return deployment
