from idact.detail.jupyter_app.format_deployments_info import \
    format_deployments_info


def test_format_deployments_info():
    formatted = format_deployments_info(cluster_name='cluster1')
    assert formatted == (
        "\nTo access the allocation and notebook deployments from cluster,"
        " you can use the following snippet.\n"
        "You may need to change the cluster name if it's different in"
        " the target environment.\n"
        "----------------\n"
        "from idact import show_cluster\n"
        "cluster = show_cluster('cluster1')\n"
        "deployments = cluster.pull_deployments()\n"
        "nodes = deployments.nodes[-1]\n"
        "nb = deployments.jupyter_deployments[-1]\n"
        "----------------")
