from datetime import timedelta
from typing import Sequence

from idact.detail.helper.utc_now import utc_now
from idact.detail.nodes.node_internal import NodeInternal


def get_expiration_date_from_nodes(nodes: Sequence[NodeInternal]):
    """Returns the earliest allocation end date, or a datetime one day
        from now.

        :param nodes: Nodes to get an expiration date from.

    """
    expiration_dates = [node.allocated_until
                        for node in nodes
                        if node.allocated_until is not None]
    if expiration_dates:
        expiration_date = min(expiration_dates)
    else:
        expiration_date = utc_now() + timedelta(days=1)

    return expiration_date
