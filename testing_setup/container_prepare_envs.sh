#!/bin/bash
# Usage: source prepare_container_envs.sh

if [ -z ${SLURM_CENTOS_VERSION} ]; then
    export SLURM_CENTOS_VERSION=7
fi
if [ -z ${SLURM_VERSION} ]; then
    export SLURM_VERSION=17.02.10
fi
if [ -z ${SLURM_USERS} ]; then
    export SLURM_USERS=100
fi
if [ -z ${SLURM_SSH_PORT} ]; then
    export SLURM_SSH_PORT=2222
fi

export SLURM_IMAGE=giovtorres/docker-centos${SLURM_CENTOS_VERSION}-slurm:${SLURM_VERSION}
export SLURM_CONTAINER=slurm-docker
