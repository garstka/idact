from enum import Enum


class SerializableTypes(Enum):
    """Type identifiers used by serializable types, see :class:`.Serializable`.
    """
    ALLOCATION_PARAMETERS = 0
    DEPLOYMENT_DEFINITION = 1
    DEPLOYMENT_DEFINITIONS = 2
    NODE_IMPL = 3
    NODES_IMPL = 4
    SLURM_ALLOCATION = 5
