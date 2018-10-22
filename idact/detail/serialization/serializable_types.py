from enum import Enum


class SerializableTypes(Enum):
    """Type identifiers used by serializable types, see :class:`.Serializable`.
    """
    ALLOCATION_PARAMETERS = 0
    APP_ALLOCATION_PARAMETERS = 1
    DEPLOYMENT_DEFINITION = 2
    DEPLOYMENT_DEFINITIONS = 3
    GENERIC_DEPLOYMENT = 4
    JUPYTER_DEPLOYMENT_IMPL = 5
    NODE_IMPL = 6
    NODES_IMPL = 7
    SLURM_ALLOCATION = 8
