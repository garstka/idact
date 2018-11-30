from idact.core.config import ClusterConfig
from idact.detail.deployment.deserialize_generic_deployment import \
    deserialize_generic_deployment
from idact.detail.jupyter.jupyter_deployment_impl import JupyterDeploymentImpl
from idact.detail.serialization.serializable_types import SerializableTypes


# pylint: disable=bad-continuation
def deserialize_jupyter_deployment_impl(
    config: ClusterConfig,
    uuid: str,
    serialized: dict) -> JupyterDeploymentImpl:  # noqa
    """Counterpart to :meth:`.JupyterDeploymentImpl.serialize`."""
    try:
        assert serialized['type'] == str(
            SerializableTypes.JUPYTER_DEPLOYMENT_IMPL)

        deployment = deserialize_generic_deployment(
            config=config,
            serialized=serialized['deployment'])
        tunnel = deployment.node.tunnel(there=serialized['tunnel_there'],
                                        here=serialized['tunnel_here'])
        return JupyterDeploymentImpl(
            deployment=deployment,
            tunnel=tunnel,
            token=serialized['token'],
            uuid=uuid)
    except KeyError as e:
        raise RuntimeError("Unable to deserialize.") from e
