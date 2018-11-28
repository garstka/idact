from idact.core.config import ClusterConfig
from idact.detail.deployment.generic_deployment import GenericDeployment
from idact.detail.nodes.node_impl import NodeImpl
from idact.detail.serialization.serializable_types import SerializableTypes


def deserialize_generic_deployment(config: ClusterConfig,
                                   serialized: dict) -> GenericDeployment:
    """Counterpart to :meth:`.GenericDeployment.serialize`."""
    try:
        assert serialized['type'] == str(
            SerializableTypes.GENERIC_DEPLOYMENT)
        return GenericDeployment(
            node=NodeImpl.deserialize(config=config,
                                      serialized=serialized['node']),
            pid=serialized['pid'],
            runtime_dir=serialized['runtime_dir'])
    except KeyError as e:
        raise RuntimeError("Unable to deserialize.") from e
