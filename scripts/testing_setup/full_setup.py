#!/usr/bin/env python3
"""Runs the container used for testing."""

import os
import subprocess

REPO_NAME = "garstka/idact-test-environment"


def get_branch_name():
    return (
        "centos{CENTOS_VERSION}"
        "-slurm{SLURM_VERSION}"
        "-py{REMOTE_PYTHON_VERSION}"
    ).format(
        CENTOS_VERSION=os.environ['CENTOS_VERSION'],
        SLURM_VERSION=os.environ['SLURM_VERSION'],
        REMOTE_PYTHON_VERSION=os.environ['REMOTE_PYTHON_VERSION'])


def get_tag_name():
    branch_name = get_branch_name()
    lastest_tag = "{branch_name}-latest".format(branch_name=branch_name)
    return os.environ.get("IDACT_CONTAINER_OVERRIDE_TAG", lastest_tag)


def get_image_name():
    return "{REPO_NAME}:{tag_name}".format(REPO_NAME=REPO_NAME,
                                           tag_name=get_tag_name())


def get_run_command():
    port_mapping = "{IDACT_TEST_CONTAINER_SSH_PORT}:22".format(
        IDACT_TEST_CONTAINER_SSH_PORT=os.environ[
            'IDACT_TEST_CONTAINER_SSH_PORT'])
    return ['docker', 'run', '-d', '-p', port_mapping, '-it', '-h', 'ernie',
            '--name', os.environ['IDACT_TEST_CONTAINER'], get_image_name()]


def main():
    subprocess.check_call(get_run_command())


if __name__ == '__main__':
    main()
