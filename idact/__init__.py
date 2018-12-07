# -*- coding: utf-8 -*-

"""
idact package
=============

Top-level package for Interactive Data Analysis Convenience Tools.

All user facing API can be imported directly from the :mod:`idact` module.

"""
from idact.core.auth import AuthMethod, KeyType
from idact.core.config import ClusterConfig, SetupActionsConfig, RetryConfig
from idact.core.dask_deployment import DaskDiagnostics, DaskDeployment
from idact.core.deploy_dask import deploy_dask
from idact.core.environment import load_environment, save_environment, \
    pull_environment, push_environment
from idact.core.get_default_retries import get_default_retries
from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.node_resource_status import NodeResourceStatus
from idact.core.node import Node
from idact.core.nodes import Nodes
from idact.core.remove_cluster import remove_cluster
from idact.core.retry import Retry
from idact.core.set_log_level import set_log_level
from idact.core.set_retry import set_retry
from idact.core.show_clusters import show_cluster, show_clusters
from idact.core.synchronized_deployments import SynchronizedDeployments
from idact.core.tunnel import Tunnel
from idact.core.walltime import Walltime
from idact.core.add_cluster import add_cluster
from idact.core.cluster import Cluster

__author__ = """Matt Garstka"""
__email__ = 'matt@garstka.net'
__version__ = '0.5.1'

_IMPORTED = {add_cluster,
             load_environment,
             save_environment,
             show_cluster,
             show_clusters,
             AuthMethod,
             Cluster,
             Walltime,
             Node,
             Nodes,
             Tunnel,
             JupyterDeployment,
             KeyType,
             set_log_level,
             ClusterConfig,
             SetupActionsConfig,
             DaskDiagnostics,
             DaskDeployment,
             deploy_dask,
             remove_cluster,
             pull_environment,
             push_environment,
             NodeResourceStatus,
             SynchronizedDeployments,
             RetryConfig,
             get_default_retries,
             Retry,
             set_retry}
"""List of the public API members imported into the top level package
    for convenience."""


def _patch_modules_for_sphinx():
    """Sphinx looks at the __module__ attribute to determine the module
        of a class, function, etc. while generating documentation.

        This value does not change after importing the object into the top
        level package, even if this effectively makes the object its member.

        In order for Sphinx to show the imported objects as members
        of the top level package, the __module__ attribute is changed manually
        for all imported objects.
    """
    for imported in _IMPORTED:
        imported.__module__ = 'idact'


_patch_modules_for_sphinx()
