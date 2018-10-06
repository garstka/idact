"""This module contains the implementation of an object for reading contents
    of an sshd port info file."""

from collections import defaultdict

from idact.detail.log.get_logger import get_logger

PORT_INFO_LOCATION = "~/.idact/sshd_ports"
PORT_INFO_DIR_NAME_FORMAT = "alloc-{allocation_id}"

NODE_DEFAULT_PORT = 22


class SshdPortInfo:
    """Determines the sshd listening port based on the contents of a directory
        written to by entry points.

        See :func:`.get_entry_point_script_contents`.

        :param contents: Directory contents.

    """

    def __init__(self, contents: str):
        self._hosts = defaultdict(list)

        log = get_logger(__name__)
        log.debug("Sshd port directory contents: %s", contents)

        lines = [i for i in contents.split(' ') if i]
        for line in lines:
            split = line.split(':')
            host = split[0]
            port = int(split[1])
            self._hosts[host].append(port)
            log.debug("Host %s at %d", host, port)

        self._hosts = dict(self._hosts)

        if not self._hosts:
            log.warning("No deployed sshd servers were reported.")

    def get_port(self,
                 host: str,
                 raise_on_missing: bool) -> int:
        """Returns the ssh access port for the host.
            Tries to provide defaults if none found.

            :param host: Host to find the ssh port for.

            :param raise_on_missing: Raise an exception on missing port info.

        """
        log = get_logger(__name__)

        if host in self._hosts and self._hosts[host]:
            return self._hosts[host].pop()
        log.warning(
            "Unable to find unique sshd server for %s", host)
        if raise_on_missing:
            raise RuntimeError(
                "Unable to find unique sshd server for {}".format(host))
        if self._hosts:
            log.warning("Assuming sandbox, defaulting to first found."
                        " If this is not sandbox, node access may not work"
                        " properly.")
            port = self._hosts[next(iter(self._hosts.keys()))][0]
            log.info("First found: %d", port)
            return port
        log.warning(
            "No port info found, defaulting to %d.", NODE_DEFAULT_PORT)
        return NODE_DEFAULT_PORT
