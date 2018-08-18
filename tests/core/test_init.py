"""Tests for core imports."""

from idact.core.set_log_level import set_log_level
from idact.core.nodes import Node, Nodes
from idact.core.auth import AuthMethod, KeyType
from idact.core.cluster import Cluster
from idact.core.add_cluster import add_cluster
from idact.core.show_clusters import show_cluster, show_clusters
from idact.core.walltime import Walltime
from idact.core.environment import load_environment, save_environment
from idact.core.tunnel import Tunnel
from idact.core.jupyter_deployment import JupyterDeployment
from idact.core.config import ClusterConfig, SetupActionsConfig
from idact.core.dask_deployment import DaskDeployment, DaskDiagnostics
from idact.core.deploy_dask import deploy_dask
from idact import _IMPORTED
from idact import add_cluster as add_cluster2
from idact import show_cluster as show_cluster2
from idact import show_clusters as show_clusters2
from idact import load_environment as load_environment2
from idact import save_environment as save_environment2
from idact import AuthMethod as AuthMethod2
from idact import Cluster as Cluster2
from idact import Node as Node2
from idact import Nodes as Nodes2
from idact import Walltime as Walltime2
from idact import Tunnel as Tunnel2
from idact import JupyterDeployment as JupyterDeployment2
from idact import KeyType as KeyType2
from idact import set_log_level as set_log_level2
from idact import ClusterConfig as ClusterConfig2
from idact import SetupActionsConfig as SetupActionsConfig2
from idact import DaskDiagnostics as DaskDiagnostics2
from idact import DaskDeployment as DaskDeployment2
from idact import deploy_dask as deploy_dask2

IMPORT_PAIRS_CORE_MAIN = [(add_cluster, add_cluster2),
                          (show_cluster, show_cluster2),
                          (show_clusters, show_clusters2),
                          (load_environment, load_environment2),
                          (save_environment, save_environment2),
                          (AuthMethod, AuthMethod2),
                          (Cluster, Cluster2),
                          (Node, Node2),
                          (Nodes, Nodes2),
                          (Walltime, Walltime2),
                          (Tunnel, Tunnel2),
                          (JupyterDeployment, JupyterDeployment2),
                          (KeyType, KeyType2),
                          (set_log_level, set_log_level2),
                          (ClusterConfig, ClusterConfig2),
                          (SetupActionsConfig, SetupActionsConfig2),
                          (DaskDiagnostics, DaskDiagnostics2),
                          (DaskDeployment, DaskDeployment2),
                          (deploy_dask, deploy_dask2)]

CORE_IMPORTS = [add_cluster,
                load_environment,
                save_environment,
                show_cluster,
                show_clusters,
                AuthMethod,
                Cluster,
                Node,
                Nodes,
                Walltime,
                Tunnel,
                JupyterDeployment,
                KeyType,
                set_log_level,
                ClusterConfig,
                SetupActionsConfig,
                DaskDiagnostics,
                DaskDeployment,
                deploy_dask]


def test_aliases():
    """Tests classes and functions imported from the core package
       to the top level package.
    """
    assert len(_IMPORTED) == 19

    for core, main in IMPORT_PAIRS_CORE_MAIN:
        assert core is main

    main_module = 'idact'
    for core in CORE_IMPORTS:
        assert main_module == core.__module__
