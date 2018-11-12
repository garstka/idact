import datetime
from math import ceil
from typing import List

from idact.core.config import ClusterConfig
from idact.core.retry import Retry
from idact.detail.allocation.allocation_parameters import AllocationParameters
from idact.detail.entry_point.fetch_port_info import fetch_port_info
from idact.detail.entry_point.remove_port_info import remove_port_info
from idact.detail.entry_point.sshd_port_info import SshdPortInfo
from idact.detail.helper.retry import retry_with_config
from idact.detail.helper.stage_info import stage_debug
from idact.detail.log.get_logger import get_logger
from idact.detail.nodes.node_impl import NodeImpl


def determine_ports_for_nodes(allocation_id: int,
                              hostnames: List[str],
                              config: ClusterConfig,
                              raise_on_missing: bool) -> List[int]:
    """Tries to determine sshd ports for each node.
        Removes the file if no exception was raised.

        :param allocation_id: Job id.

        :param hostnames: List of hostnames.

        :param config: Cluster config.

        :param raise_on_missing: Raise an exception if port could not
                                 be determined.

    """
    log = get_logger(__name__)
    with stage_debug(log, "Fetching port info for sshd."):
        port_info_contents = fetch_port_info(allocation_id=allocation_id,
                                             config=config)
        port_info = SshdPortInfo(contents=port_info_contents)

    with stage_debug(log, "Determining ports for each host."):
        ports = [port_info.get_port(host=host,
                                    raise_on_missing=raise_on_missing)
                 for host in hostnames]

    with stage_debug(log, "Removing the file containing sshd port info."):
        remove_port_info(allocation_id, config=config)

    return ports


def finalize_allocation(allocation_id: int,
                        hostnames: List[str],
                        nodes: List[NodeImpl],
                        parameters: AllocationParameters,
                        allocated_until: datetime.datetime,
                        config: ClusterConfig):
    """Fetches node ports and makes them allocated.

        :param allocation_id: Allocation id, e.g. Slurm job id.

        :param hostnames: List of hostnames.

        :param nodes: Nodes to update with information.

        :param parameters: Allocation parameters.

        :param allocated_until: Timestamp for job termination.

        :param config: Cluster config.

    """

    def try_to_determine_ports():
        return determine_ports_for_nodes(allocation_id=allocation_id,
                                         hostnames=hostnames,
                                         config=config,
                                         raise_on_missing=True)

    try:
        node_count = len(hostnames)
        multiplier = int(ceil(node_count / 10))
        ports = retry_with_config(try_to_determine_ports,
                                  name=Retry.PORT_INFO,
                                  config=config,
                                  multiplier=multiplier)
    except RuntimeError:
        ports = determine_ports_for_nodes(allocation_id=allocation_id,
                                          hostnames=hostnames,
                                          config=config,
                                          raise_on_missing=False)

    for host, port, node in zip(hostnames, ports, nodes):
        node.make_allocated(
            host=host,
            port=port,
            cores=parameters.cores,
            memory=parameters.memory_per_node,
            allocated_until=allocated_until)
