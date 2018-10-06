from contextlib import ExitStack

import pytest
from bitmath import MiB

from idact import Walltime, show_cluster, Node
from idact.detail.auth.set_password import set_password
from idact.detail.deployment.cancel_on_exit import cancel_on_exit
from idact.detail.helper.remove_runtime_dir import remove_runtime_dir
from tests.helpers.disable_pytest_stdin import disable_pytest_stdin
from tests.helpers.reset_environment import reset_environment
from tests.helpers.set_up_key_location import set_up_key_location
from tests.helpers.test_users import USER_15, get_test_user_password
from tests.helpers.testing_environment import TEST_CLUSTER


def check_will_remove_empty(node: Node):
    # will remove an empty dir
    node.run("mkdir dir1")
    node.run("ls dir1")
    remove_runtime_dir(node=node,
                       runtime_dir="dir1")
    with pytest.raises(RuntimeError):
        node.run("ls dir1")


def check_will_ignore_non_existent(node: Node):
    # will ignore non-existent dir
    with pytest.raises(RuntimeError):
        node.run("ls dir2")
    remove_runtime_dir(node=node,
                       runtime_dir="dir2")


def check_will_remove_files(node: Node):
    # will remove a dir with files in it
    node.run("mkdir dir3")
    node.run("touch dir3/file1")
    node.run("touch dir3/file2")
    node.run("ls dir3")
    remove_runtime_dir(node=node,
                       runtime_dir="dir3")
    with pytest.raises(RuntimeError):
        node.run("ls dir3")


def check_will_not_remove_dotfiles(node: Node):
    # will not remove a dir when there are dot files
    # but non-dotfiles will be removed
    node.run("mkdir dir4")
    node.run("touch dir4/file1")
    node.run("touch dir4/file2")
    node.run("touch dir4/.file3")
    node.run("ls dir4")
    remove_runtime_dir(node=node,
                       runtime_dir="dir4")
    node.run("ls dir4")
    node.run("ls dir4/.file3")
    with pytest.raises(RuntimeError):
        node.run("ls dir4/file1")
    with pytest.raises(RuntimeError):
        node.run("ls dir4/file2")


def check_will_not_remove_nested_dirs(node: Node):
    # will not remove nested dirs or their content
    # but regular files will be removed
    node.run("mkdir dir5")
    node.run("touch dir5/file1")
    node.run("touch dir5/file2")
    node.run("mkdir dir5/subdir1")
    node.run("touch dir5/subdir1/file3")
    node.run("ls dir5")
    remove_runtime_dir(node=node,
                       runtime_dir="dir4")
    node.run("ls dir5")
    node.run("ls dir5/subdir1")
    node.run("ls dir5/subdir1/file3")
    with pytest.raises(RuntimeError):
        node.run("ls dir4/file1")
    with pytest.raises(RuntimeError):
        node.run("ls dir4/file2")


def test_remove_runtime_dir_test():
    user = USER_15
    with ExitStack() as stack:
        stack.enter_context(set_up_key_location())
        stack.enter_context(disable_pytest_stdin())
        stack.enter_context(reset_environment(user))
        stack.enter_context(set_password(get_test_user_password(user)))

        cluster = show_cluster(name=TEST_CLUSTER)
        nodes = cluster.allocate_nodes(nodes=1,
                                       cores=1,
                                       memory_per_node=MiB(100),
                                       walltime=Walltime(minutes=30))
        stack.enter_context(cancel_on_exit(nodes))
        node = nodes[0]
        try:
            nodes.wait(timeout=10)
            assert nodes.running()

            check_will_remove_empty(node=node)
            check_will_ignore_non_existent(node=node)
            check_will_remove_files(node=node)
            check_will_not_remove_dotfiles(node=node)
            check_will_not_remove_nested_dirs(node=node)
        finally:
            node.run("rm -rf *")
