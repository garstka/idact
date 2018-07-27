"""Contents of this module are intended to be imported into
   the top-level package.

   See :class:`.Cluster`.
"""

from abc import ABC, abstractmethod
from typing import Union, Optional, Dict

import bitmath

from idact.core.nodes import Nodes, Node
from idact.core.walltime import Walltime


class Cluster(ABC):
    """Remote cluster interface."""

    @abstractmethod
    def allocate_nodes(self,
                       nodes: int = 1,
                       cores: int = 1,
                       memory_per_node: Union[str, bitmath.Byte] = None,
                       walltime: Union[str, Walltime] = None,
                       native_args: Optional[Dict[str, Optional[
                           str]]] = None) -> Nodes:  # noqa, pylint: disable=bad-whitespace,line-too-long
        """Tries to allocate nodes with the given parameters.

            :param nodes:
                * Cluster node count.
                * Default: 1
            :param cores:
                * CPU core count per node.
                * Default: 1
            :param memory_per_node:
                * Memory per node.
                * Can be parsed from string, or as a bitmath unit,
                  e.g. MiB(500), MB(500), GiB(24), GB(24).
                * Default: `bitmath.GiB(1)`
            :param walltime:
                * Maximum time to allocate the resources for.
                * Can be a string, e.g. '1-2:30:00'
                  (1 day, 2 hours, 30 minutes, 0 seconds).
                * For the correct string format,
                  see :meth:`.Walltime.from_string`
                * Can be a :class:`.Walltime`,
                  e.g. `Walltime(days=1, hours=2, minutes=30)`
                * Default: `Walltime(minutes=10)`
            :param native_args:
                * Native arguments for the workload manager.
                * Values are not validated.
                * Native arguments take precedence over other arguments.
                * Arguments with None as value are treated as flags.
        """
        pass

    @abstractmethod
    def get_access_node(self) -> Node:
        """Returns the cluster head node, which does not require allocation."""
        pass
