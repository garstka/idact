from idact.core.nodes import Node
from idact.detail.dask.dask_scheduler_deployment import DaskSchedulerDeployment
from idact.detail.helper.check_address_reachable_from_node import \
    check_address_reachable_from_node


def check_scheduler_reachable(node: Node,
                              scheduler: DaskSchedulerDeployment):
    """Checks whether the scheduler is reachable from the node.

        :param node: Node to check connectivity from.

        :param scheduler: Scheduler to connect to.

    """
    scheduler_address = scheduler.address

    _, slashes_ip_address, port = scheduler_address.split(':')
    _, ip_address = slashes_ip_address.split('//')

    check_address_reachable_from_node(node,
                                      ip_address=ip_address,
                                      port=int(port))
