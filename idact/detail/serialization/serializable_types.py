from enum import Enum


class SerializableTypes(Enum):
    """Type identifiers used by serializable types, see :class:`.Serializable`.
    """
    ALLOCATION_PARAMETERS = 0
    DEPLOYMENT_DEFINITION = 1
    DEPLOYMENT_DEFINITIONS = 2
    GENERIC_DEPLOYMENT = 3
    JUPYTER_DEPLOYMENT_IMPL = 4
    NODE_IMPL = 5
    NODES_IMPL = 6
    SLURM_ALLOCATION = 7
