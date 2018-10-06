# Changelog

## 0.3

Multiple stability and debugability improvements, among them:
 - More task stage info is available for the user.
 - More actions are retried on failure.
 - Conda dev environment and pip install and are now tested on Travis.

## 0.2

Added:
 - Deployment of Jupyter Notebook on allocated nodes.
 - Deployment of Dask on allocated nodes.
 - Support for public key authentication.
 - A way to push and pull the environment from local machine to cluster.
 - A way to examine CPU and memory usage of a node.
 - A notebook for testing functionality on the Prometheus cluster (ProSandbox.ipynb).
 - Tunneling of remote node ports to local ports.
 - A way to set log level.
 - Support for Python 3.5.

## 0.1

Initial release.
 - Added basic node allocation with password authentication.
 - Added a way to save and load the environment.
