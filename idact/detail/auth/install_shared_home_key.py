from fabric.contrib.files import exists
from fabric.operations import run
import fabric.decorators
import fabric.tasks

from idact.detail.helper.raise_on_remote_fail import raise_on_remote_fail
from idact.detail.log.get_logger import get_logger

SHARED_HOST_KEY_PATH = "~/.ssh/ssh_host_rsa_key"


def install_shared_home_key():
    """Installs shared home host key on access node as a in order to allow
        public key authentication between the access node and cluster nodes
        after sshd deployment.

        If any of the keys was not generated, it will be generated at this
        point.
        Expects authentication to have already been performed.
    """
    log = get_logger(__name__)

    @fabric.decorators.task
    def task():
        run("mkdir -p ~/.ssh")
        run("chmod 700 ~/.ssh")
        if not exists(SHARED_HOST_KEY_PATH):
            log.info("Generating shared host key...")
            run("ssh-keygen"
                " -t rsa"
                " -f {shared_host_key_path}"
                " -N ''".format(shared_host_key_path=SHARED_HOST_KEY_PATH))

    with raise_on_remote_fail(exception=RuntimeError):
        fabric.tasks.execute(task)
