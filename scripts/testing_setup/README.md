# Testing setup

The `testing_setup` directory contains scripts for running a test container with Slurm
with ssh access ([idact-test-environment](https://github.com/garstka/idact-test-environment)).


## Requirements

Docker on Linux, Internet access.

## Usage

```
source container_prepare_envs.sh
python full_setup.py
(...)
python full_teardown.py
```

## Attach root console

```
docker attach idact-test-container
```

## Ssh as user

```
ssh -o "StrictHostKeyChecking no" -p $IDACT_TEST_CONTAINER_SSH_PORT user-1@localhost
```

Password corresponds to user number, in this case: pass-1

## Use ssh keys

```
ssh-keygen -t rsa
ssh-copy-id -o "StrictHostKeyChecking no" -i ~/.ssh/id_rsa.pub -p $IDACT_TEST_CONTAINER_SSH_PORT user-1@localhost
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

Sample port forwarding from Windows:

```
putty -N -L 8080:localhost:8080 user-1@localhost -P 2222
```

### Possible problem

 - When using port forwarding for testing, the key fingerprint of the server
  may need to be manually removed from `known_hosts` (or the equivalent)
  after a setup-teardown cycle.
 - On Linux, this is taken care of by the setup script.
