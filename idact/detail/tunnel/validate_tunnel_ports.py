from typing import Optional, Tuple

from idact.detail.config.validation.validate_port import validate_port
from idact.detail.helper.is_local_port_taken import is_local_port_taken
from idact.detail.log.get_logger import get_logger

ANY_PORT = 0


def validate_tunnel_ports(here: Optional[int],
                          there: int) -> Tuple[int, int]:
    """Validates port tunnels, provides fallback if local port is taken.
        Returns valid values.

        :param here: Local port.
        :param there: Remote port.

    """
    log = get_logger(__name__)

    validate_port(there)
    if here is None:
        here = ANY_PORT
        log.info("No local port specified for tunnel, binding"
                 " to any free port.")
    elif here != ANY_PORT:
        validate_port(here)
        if is_local_port_taken(port=here):
            log.info("Desired local tunnel port %d is taken."
                     " Binding to random port instead.", here)
            here = ANY_PORT
    return here, there
