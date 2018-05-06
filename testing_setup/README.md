# Testing setup

This directory contains scripts for running a testing container with SLURM and
access via ssh.

## Requirements

Docker on Linux, Internet access.

## Usage

```
source container_defaults.sh
source prepare_container_envs.sh
python container_setup.py
(...)
python container_teardown.py
```

## Attach root console

```
docker attach slurm-docker
```

## Ssh as user

```
ssh -o "StrictHostKeyChecking no" -p $SLURM_SSH_PORT user-1@localhost
```

Password corresponds to user number, in this case: pass-1

## Use ssh keys

```
ssh-keygen -t rsa
ssh-copy-id -o "StrictHostKeyChecking no" -i ~/.ssh/id_rsa.pub -p $SLURM_SSH_PORT user-1@localhost
```
