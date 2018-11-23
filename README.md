# Welcome to idact!

[![Build Status](https://travis-ci.com/garstka/idact.svg?token=cvggfL1vjmB383MxWGF4&branch=master)](https://travis-ci.com/garstka/idact)
[![Build Status](https://travis-ci.com/garstka/idact.svg?token=cvggfL1vjmB383MxWGF4&branch=develop)](https://travis-ci.com/garstka/idact)

Idact, or *Interactive Data Analysis Convenience Tools*, is a Python 3.5+ library
that takes care of several tedious aspects of working with big data
on an HPC cluster.

## Who is it for?

Data scientists or big data enthusiasts, who:
 - Perform computations on [Jupyter Notebook](http://jupyter.org/),
  using libraries such as [NumPy](http://www.numpy.org/),
  [pandas](https://pandas.pydata.org/),
  [Matplotlib](https://matplotlib.org/),
  or [bokeh](https://bokeh.pydata.org/en/latest/).
 - Have access to an HPC cluster with [Slurm](https://slurm.schedmd.com/)
  as the job scheduler.
 - Would like to parallelize their computations across many nodes using
  [Dask.distributed](http://distributed.dask.org/en/latest/), a library
  for distributed computing.
 - May find that it takes too much manual effort to deploy Jupyter Notebook
  and Dask on the cluster each time they need it.

## Requirements

Python 3.5+.

### Client

 - Operating System: Windows or Linux
 - Recommended: [Jupyter Notebook](http://jupyter.org/)
  or [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/index.html)

### Cluster

 - Operating System: Linux
 - Job Scheduler: [Slurm Workload Manager](https://slurm.schedmd.com/)
 - SSH access to a login (head) node.
 - [Dask.distributed](http://distributed.dask.org/en/latest/)
 - [Jupyter Notebook](http://jupyter.org/)
  or [JupyterLab](https://jupyterlab.readthedocs.io/en/stable/index.html)

## Installation

```
python -m pip install idact
```

## Code samples

### Accessing a cluster

Cluster can be accessed with a public/private key pair via SSH.

```python
from idact import *
cluster = add_cluster(name="my-cluster",
                      user="user",
                      host="localhost",
                      port=2222,
                      auth=AuthMethod.PUBLIC_KEY,
                      key="~/.ssh/id_rsa",
                      install_key=False)
node = cluster.get_access_node()
node.connect()
```

### Allocating and deallocating nodes

Nodes are allocated as a Slurm job.
Afterwards, they can be used for deployments.

```python
import bitmath
nodes = cluster.allocate_nodes(nodes=8,
                               cores=12,
                               memory_per_node=bitmath.GiB(120),
                               walltime=Walltime(hours=1, minutes=30),
                               native_args={
                                   '--partition': 'debug',
                                   '--account': 'data-analysis-group'
                               })
try:
    nodes.wait(timeout=120.0)
except TimeoutError:
    nodes.cancel()
```

### Deploying Jupyter Notebook

Jupyter Notebook is deployed on a cluster node,
and made accessible through an SSH tunnel.

```python
nb = nodes[0].deploy_notebook()
nb.open_in_browser()
```

### Deploying Dask.distributed

Dask.distributed scheduler and workers are deployed
on cluster nodes, and their dashboards are made available
through SSH tunnels.

```python
dd = deploy_dask(nodes[1:])
client = dd.get_client()
client.submit(...)
dd.diagnostics.open_all()
```

### Managing cluster config

Local and remote cluster configuration can be saved, loaded,
and copied to and from the cluster.

```python
save_environment()
load_environment()

push_environment()
pull_environment()
```

### Managing deployments

Deployment objects can be serialized between running program
instances, local or remote.

```python
push_deployment(nodes)
push_deployment(nb)
push_deployment(dd)

pull_deployments()
```

## Documentation

The documentation contains detailed API description, tutorial notebooks,
and other helpful information.

 - [Documentation - master](https://garstka.github.io/idact/master/html/index.html)
 - [Documentation - develop](https://garstka.github.io/idact/develop/html/index.html)
 - [All versions](https://garstka.github.io/idact/develop/html/docs_by_version.html)

## Source code

The source code is available on [GitHub](https://github.com/garstka/idact).

## License

MIT License.

This library was developed under the supervision of Leszek Grzanka, PhD
as a final project of the BEng in Computer Science program
at the Faculty of Computer Science, Electronics and Telecommunications
at AGH University of Science and Technology, Krakow.
