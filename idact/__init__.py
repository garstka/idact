# -*- coding: utf-8 -*-

"""Top-level package for Interactive Data Analysis Convenience Tools."""
from idact.core.auth import AuthMethod
from idact.core.environment import load_environment, save_environment
from idact.core.nodes import Nodes, Node
from idact.core.show_clusters import show_cluster, show_clusters
from idact.core.walltime import Walltime
from idact.core.add_cluster import add_cluster
from idact.core.cluster import Cluster

__author__ = """Matt Garstka"""
__email__ = 'matt.garstka@gmail.com'
__version__ = '0.1.0'

_IMPORTED = {add_cluster,
             load_environment,
             save_environment,
             show_cluster,
             show_clusters,
             AuthMethod,
             Cluster,
             Walltime,
             Node,
             Nodes}


def _patch_modules_for_sphinx():
    for imported in _IMPORTED:
        imported.__module__ = 'idact'


_patch_modules_for_sphinx()
