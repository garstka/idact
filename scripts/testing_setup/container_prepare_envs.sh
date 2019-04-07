#!/bin/bash
# Usage: source prepare_container_envs.sh

if [ -z ${CENTOS_VERSION} ]; then
    export CENTOS_VERSION=7
fi
if [ -z ${SLURM_VERSION} ]; then
    export SLURM_VERSION=17.02.10
fi
if [ -z ${REMOTE_PYTHON_VERSION} ]; then
    export REMOTE_PYTHON_VERSION=3.6
fi
if [ -z ${IDACT_TEST_CONTAINER_SSH_PORT} ]; then
    export IDACT_TEST_CONTAINER_SSH_PORT=2222
fi
if [ -z ${IDACT_TEST_CONTAINER} ]; then
    export IDACT_TEST_CONTAINER=idact-test-container
fi
