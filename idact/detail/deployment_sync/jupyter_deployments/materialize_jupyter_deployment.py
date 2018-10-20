from idact.core.config import ClusterConfig
from idact.detail.deployment_sync.deployment_definition import \
    DeploymentDefinition
from idact.detail.jupyter.deserialize_jupyter_deployment_impl import \
    deserialize_jupyter_deployment_impl
from idact.detail.jupyter.jupyter_deployment_impl import JupyterDeploymentImpl


# pylint: disable=bad-continuation
def materialize_jupyter_deployment(
    config: ClusterConfig,
    uuid: str,
    definition: DeploymentDefinition) -> JupyterDeploymentImpl:  # noqa
    """Materializes the Jupyter deployment definition.

        :param config:      Cluster to materialize the Jupyter deployment with.
        :param uuid:        Unique deployment id.
        :param definition:  Deployment definition to materialize.

    """
    jupyter_deployment = deserialize_jupyter_deployment_impl(
        config=config,
        uuid=uuid,
        serialized=definition.value)
    return jupyter_deployment
