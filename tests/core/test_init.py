from idact.core.nodes import Node, Nodes
from idact.core.auth import AuthMethod
from idact.core.cluster import Cluster
from idact.core.add_cluster import add_cluster
from idact.core.show_clusters import show_cluster, show_clusters
from idact.core.walltime import Walltime
from idact.core.environment import load_environment, save_environment
from idact.core.tunnel import Tunnel
from idact.core.jupyter_deployment import JupyterDeployment
from idact import _IMPORTED


def test_aliases():
    """Tests classes and functions imported from the core package
       to the top level package.
    """
    assert len(_IMPORTED) == 12
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

    assert add_cluster is add_cluster2
    assert show_cluster is show_cluster2
    assert show_clusters is show_clusters2
    assert load_environment is load_environment2
    assert save_environment is save_environment2
    assert AuthMethod is AuthMethod2
    assert Cluster is Cluster2
    assert Node is Node2
    assert Nodes is Nodes2
    assert Walltime is Walltime2
    assert Tunnel is Tunnel2
    assert JupyterDeployment is JupyterDeployment2

    main_module = 'idact'
    assert main_module == add_cluster.__module__
    assert main_module == load_environment.__module__
    assert main_module == save_environment.__module__
    assert main_module == show_cluster.__module__
    assert main_module == show_clusters.__module__
    assert main_module == AuthMethod.__module__
    assert main_module == Cluster.__module__
    assert main_module == Node.__module__
    assert main_module == Nodes.__module__
    assert main_module == Walltime.__module__
    assert main_module == Tunnel.__module__
    assert main_module == JupyterDeployment.__module__
