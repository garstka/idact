SNIPPET_SEPARATOR_LENGTH = 16


def format_deployments_info(cluster_name: str) -> str:
    """Formats text that informs the user they can pull
        the new deployments, with a snippet.

        :param cluster_name: Cluster name to use.

    """

    result = "\n"
    result += ("To access the allocation and notebook deployments"
               " from cluster, you can use the following snippet.\n")
    result += ("You may need to change the cluster name"
               " if it's different in the target environment.\n")
    result += ("-" * SNIPPET_SEPARATOR_LENGTH) + "\n"
    result += "from idact import show_cluster\n"
    result += ("cluster = show_cluster('{cluster_name}')\n".format(
        cluster_name=cluster_name))
    result += "deployments = cluster.pull_deployments()\n"
    result += "nodes = deployments.nodes[-1]\n"
    result += "nb = deployments.jupyter_deployments[-1]\n"
    result += ("-" * SNIPPET_SEPARATOR_LENGTH)
    return result
