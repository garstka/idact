"""This module contains functionality for creating a scratch directory
    on a cluster."""

import shlex

from idact.detail.nodes.node_internal import NodeInternal

SCRATCH_SUBDIR = ".idact-scratch"


def get_scratch_from_environment_variable(node: NodeInternal) -> str:
    """Returns the scratch path by getting the value of the environment
        variable defined in config.

        :param node: Node to get the environment variable from.

    """
    assert node.config.scratch.startswith('$')
    variable_name = node.config.scratch[1:]
    variable_name_quoted = shlex.quote(variable_name)
    scratch = node.run("printenv {}".format(variable_name_quoted))
    return scratch


def create_scratch_subdir(node: NodeInternal) -> str:
    """Creates and returns the path to a scratch subdirectory on this node.

        The created dir is a subdirectory of :meth:`.ClusterConfig.scratch`.
        It is not unique to a deployment, Dask takes care of that.

        :param node: Node to create the scratch subdir on.

    """
    if node.config.scratch.startswith('/'):
        scratch = node.config.scratch
    else:
        scratch = get_scratch_from_environment_variable(node=node)

    scratch_subdir = shlex.quote(
        "{scratch}/{subdir}".format(
            scratch=scratch,
            subdir=SCRATCH_SUBDIR))
    node.run("mkdir -p {}".format(scratch_subdir))
    node.run("chmod 700 {}".format(scratch_subdir))
    scratch_subdir_realpath = node.run("readlink -vf {}".format(
        scratch_subdir))

    return scratch_subdir_realpath
