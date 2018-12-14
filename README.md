# Welcome to idact!

[![Build Status - master](https://travis-ci.com/garstka/idact.svg?token=cvggfL1vjmB383MxWGF4&branch=master)](https://travis-ci.com/garstka/idact)
[![Build Status - develop](https://travis-ci.com/garstka/idact.svg?token=cvggfL1vjmB383MxWGF4&branch=develop)](https://travis-ci.com/garstka/idact)
[![Coverage Status - master](https://coveralls.io/repos/github/garstka/idact/badge.svg?branch=master)](https://coveralls.io/github/garstka/idact?branch=master)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/idact.svg)](https://pypi.org/project/idact/)
[![PyPI - License](https://img.shields.io/pypi/l/idact.svg)](https://pypi.org/project/idact/)
[![PyPI](https://img.shields.io/pypi/v/idact.svg)](https://pypi.org/project/idact/)

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
 - Shared $HOME directory between nodes.
 - [Dask.distributed](http://distributed.dask.org/en/latest/) with [bokeh](https://bokeh.pydata.org/en/latest/).
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

Tutorial:
[01. Connecting to a cluster](https://garstka.github.io/idact/develop/html/_notebooks/01-Connecting_to_a_cluster.html)

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

Tutorial:
[02. Allocating nodes](https://garstka.github.io/idact/develop/html/_notebooks/02-Allocating_nodes.html)

### Deploying Jupyter Notebook

Jupyter Notebook is deployed on a cluster node,
and made accessible through an SSH tunnel.

```python
nb = nodes[0].deploy_notebook()
nb.open_in_browser()
```

Tutorial:
[03. Deploying Jupyter](https://garstka.github.io/idact/develop/html/_notebooks/03-Deploying_Jupyter.html)

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

Tutorial:
[04. Deploying Dask](https://garstka.github.io/idact/develop/html/_notebooks/04-Deploying_Dask.html),
[09. Demo analysis](https://garstka.github.io/idact/develop/html/_notebooks/09a-Demo_analysis_-_local_part.html)

### Managing cluster config

Local and remote cluster configuration can be saved, loaded,
and copied to and from the cluster.

```python
save_environment()
load_environment()

push_environment(cluster)
pull_environment(cluster)
```

Tutorials:
[01. Connecting to a cluster](https://garstka.github.io/idact/develop/html/_notebooks/01-Connecting_to_a_cluster.html),
[05. Configuring idact on a cluster](https://garstka.github.io/idact/develop/html/_notebooks/05a-Configuring_idact_on_a_cluster_-_local_part.html)

### Managing deployments

Deployment objects can be serialized and copied between running program
instances, local or remote.

```python
cluster.push_deployment(nodes)
cluster.push_deployment(nb)
cluster.push_deployment(dd)

cluster.pull_deployments()
```

Tutorials:
[06. Working on a cluster](https://garstka.github.io/idact/develop/html/_notebooks/06a-Working_on_a_cluster_-_local_part.html),
[07. Adjusting timeouts](https://garstka.github.io/idact/develop/html/_notebooks/07-Adjusting_timeouts.html)

### Quick deployment app

Quick deployment app allocates nodes and deploys Jupyter notebook
from command line:

```
idact-notebook my-cluster --nodes 3 --walltime 0:20:00
```

Tutorial:
[08. Using the quick deployment app](https://garstka.github.io/idact/develop/html/_notebooks/08a-Using_the_quick_deployment_app_-_local_part.html)

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
