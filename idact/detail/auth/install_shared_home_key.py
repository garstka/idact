"""This module contains a function for generating a host key for sshd
    deployment."""

from fabric.contrib.files import exists
from fabric.operations import run
import fabric.decorators
import fabric.tasks

from idact.detail.helper.raise_on_remote_fail import raise_on_remote_fail
from idact.detail.helper.stage_info import stage_info
from idact.detail.log.capture_fabric_output_to_log import \
    capture_fabric_output_to_log
from idact.detail.log.get_logger import get_logger

SHARED_HOST_KEY_PATH = "~/.ssh/ssh_host_rsa_key"


def install_shared_home_key():
    """Installs shared home host key on access node as a in order to allow
        public key authentication between the access node and cluster nodes
        after sshd deployment.

        If the key was not generated, it will be generated at this
        point.
        Expects authentication to have already been performed.
    """
    log = get_logger(__name__)

    @fabric.decorators.task
    def task():
        """Creates the .ssh dir with proper permissions and generates the host
            key if it's not been generated already."""
        with stage_info(log, "Creating the ssh directory."):
            with capture_fabric_output_to_log():
                run("mkdir -p ~/.ssh")
                run("chmod 700 ~/.ssh")

        with capture_fabric_output_to_log():
            file_exists = exists(SHARED_HOST_KEY_PATH)

        if file_exists:
            log.debug("Skipping the generation of host key, because it"
                      " already exists: %s", SHARED_HOST_KEY_PATH)
        else:
            with stage_info(log, "Generating shared host key at %s.",
                            SHARED_HOST_KEY_PATH):
                with capture_fabric_output_to_log():
                    run(
                        "ssh-keygen"
                        " -t rsa"
                        " -f {shared_host_key_path}"
                        " -N ''".format(
                            shared_host_key_path=SHARED_HOST_KEY_PATH))

    with raise_on_remote_fail(exception=RuntimeError):
        fabric.tasks.execute(task)
