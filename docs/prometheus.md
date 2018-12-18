# Prometheus cluster

Prometheus is a cluster in ACK CYFRONET AGH, Poland.
It was used for the development of idact.
If you intend to use it, you may want to read
a basic user guide available here: [Prometheus Basics [Polish only]](https://kdm.cyfronet.pl/portal/Prometheus:Podstawy).

Otherwise, the information below may provide some insight into
some of the design choices of idact.
I attempted to highlight the most important characteristics of the cluster.

## Head node

Cluster head node can be accessed via SSH at `pro.cyfronet.pl`.
Password or public key authentication is allowed.
It's the only node on which the Slurm allocation command
([sbatch](https://slurm.schedmd.com/sbatch.html)),
can be executed.

Running calculations and other CPU-heavy operations on the head node
is not permitted. Memory limit for all processes for a given user is 6GiB.

## Compute nodes

Compute nodes can be accessed from the head node.
There is no direct access through SSH though. To perform any work
on a compute node, a Slurm job needs needs to be allocated.
You can get a list of nodes and their statuses (e.g. idle, allocated)
by running [sinfo](https://slurm.schedmd.com/sinfo.html).

There are 2160 nodes with 24 cores and 120GiB of memory available
for jobs, as detailed
[here [Polish only]](https://kdm.cyfronet.pl/portal/Prometheus).
A node can be allocated partially.

## Storage

There are a few ways to store data on the cluster. Three of them are:

 - `$HOME`: NFS-based persistent storage. Intended for personal user data.
The quota is 40GiB. Throughput is relatively low (1GiB/s).
 - `$SCRATCH`: Lustre-based temporary storage. Intended for intermediate
computation results. Data older that 30 days is removed.
The quota is 100TiB, and the throughput is much higher than `$HOME` (120GiB/s).
 - `$PLG_GROUPS_STORAGE/<group>`: Lustre-based persistent storage for groups,
not individual users. Quota is grant-dependent. The throughput is lower than
`$SCRATCH` (30GiB/s).

## Accounting

A grant id is required for job allocation, to be passed as the native `sbatch`
argument: `--account`. A user must request access to the grant resources.
An account has a finite number of CPU time assigned.
Job running time is multiplied by the number of cores used, and then by
a factor of 4. The resulting CPU time is charged to the account.

## Partitions

In general, the shorter the walltime of a job, the faster the requested
resources will be allocated.

Choosing a partition through the native `sbatch` argument `--partition` may
speed it up as well.
For instance, the partitions `plgrid-short` and `plgrid-testing` have the walltime
limit of 1 hour, but the likelyhood of a job being allocated quickly is much
higher than the default partition `plgrid`.

There is also a partition for long jobs (`plgrid-long`),
high parallelism (`plgrid-large`), and with GPU resources (`plgrid-gpu`).
