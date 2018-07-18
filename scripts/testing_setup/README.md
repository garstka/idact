# Testing setup

The `testing_setup` directory contains scripts for running a testing container with SLURM and
access via ssh.

## Requirements

Docker on Linux, Internet access.

## Usage

```
source container_defaults.sh
source container_prepare_envs.sh
python full_setup.py
(...)
python full_teardown.py
```

## Attach root console

```
docker attach slurm-docker
```

## Submit basic SLURM job

```
sbatch --wrap="sleep 10"
squeue
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

## How to run tests on Windows

For now, you will need to setup an ssh tunnel to the Linux OS with the testing
container.

### VirtualBox

Go into:
 1. Devices
 2. Network
 3. Network Settings
 4. Adapter 1
 5. Advanced
 6. Port Forwarding
 7. (plus icon)

Set up a new rule:

| Name          | Protocol | Host IP   | Host Port | Guest IP | Guest Port |
|:-------------:|:--------:|:---------:|:---------:|:--------:|:----------:|
| Testing Setup | TCP      | 127.0.0.1 | 2222      |          | 2222       |

Test the connection, e.g.:

```
putty -P 2222 user-1@localhost
```

Click "No" to skip caching the server key fingerprint, in order to avoid
the problem below.

### Possible problem

 - When using port forwarding for testing, the key fingerprint of the server
  may need to be manually removed from `known_hosts` (or the equivalent)
  after a setup-teardown cycle.
 - On Linux, this was taken care of by the setup script.

## Software installed on top of base image

### Python 3.6

```
python3.6
pip3.6
```

### Jupyter

Some Jupyter software is installed for manual testing.

#### Jupyter Notebook

To run Jupyter Notebook:

```
jupyter notebook --ip 127.0.0.1 --port 8080
```

On host machine:

```
putty -N -L 8080:localhost:8080 user-1@localhost -P 2222
```

#### Jupyter Hub

To run Jupyter Hub:

```
jupyterhub
```

On host machine:

```
putty -N -L 8000:localhost:8000 user-1@localhost -P 2222
```

#### Jupyter Lab

To run Jupyter Lab:

```
jupyter lab --ip 127.0.0.1 --port 8090
```

On host machine:

```
putty -N -L 8090:localhost:8090 user-1@localhost -P 2222
```
