from io import BytesIO

from fabric.contrib.files import exists
from fabric.operations import run, get
import fabric.decorators
import fabric.tasks

from idact.detail.helper.raise_on_remote_fail import raise_on_remote_fail
from idact.detail.log.get_logger import get_logger

SHARED_HOST_KEY_PATH = "~/.ssh/ssh_host_rsa_key"


def install_shared_home_key():
    """Installs shared home public key and host key on access node
       in order to allow public key authentication between the access node
       and cluster nodes.
       If any of the keys was not generated, it will be at this point.
       Expects password authentication to have already been performed.
    """
    log = get_logger(__name__)

    @fabric.decorators.task
    def task():
        run("mkdir -p ~/.ssh")
        run("chmod 700 ~/.ssh")
        run("touch ~/.ssh/authorized_keys")
        run("chmod 644 ~/.ssh/authorized_keys")
        if not exists("~/.ssh/id_rsa"):
            log.info("Generating key pair on access node for passwordless"
                     " connection between nodes...")
            run("ssh-keygen"
                " -t rsa"
                " -f ~/.ssh/id_rsa"
                " -N ''")
        if not exists(SHARED_HOST_KEY_PATH):
            log.info("Generating shared host key...")
            run("ssh-keygen"
                " -t rsa"
                " -f {shared_host_key_path}"
                " -N ''".format(shared_host_key_path=SHARED_HOST_KEY_PATH))

        public_key_fd = BytesIO()
        get("~/.ssh/id_rsa.pub", public_key_fd)
        public_key = public_key_fd.getvalue().decode('ascii').splitlines()[0]

        authorized_keys_fd = BytesIO()
        get("~/.ssh/authorized_keys", authorized_keys_fd)
        authorized_keys = authorized_keys_fd.getvalue().decode('ascii') \
            .splitlines()

        if public_key not in authorized_keys:
            log.info("Adding id_rsa.pub to authorized_keys on access node"
                     " for passwordless connection between nodes...")
            run("echo '{public_key}' >> ~/.ssh/authorized_keys".format(
                public_key=public_key))

    with raise_on_remote_fail(exception=RuntimeError):
        fabric.tasks.execute(task)
