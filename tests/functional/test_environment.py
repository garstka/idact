import os

from idact import show_clusters, show_cluster, add_cluster, \
    AuthMethod, save_environment, load_environment
from idact.detail.auth.set_password import set_password
from tests.helpers.clear_environment import clear_environment
from tests.helpers.reset_environment import TEST_CLUSTER
from tests.helpers.test_users import USER_2, get_password


def test_environment():
    user = USER_2
    test_environment_file = './idact.test.conf'
    with clear_environment():
        with set_password(get_password(user)):
            clusters = show_clusters()
            assert clusters == {}

            cluster = add_cluster(name=TEST_CLUSTER,
                                  user=user,
                                  host='localhost',
                                  port=os.environ.get('SLURM_PORT', 2222),
                                  auth=AuthMethod.ASK)

            clusters = show_clusters()
            assert show_cluster(name=TEST_CLUSTER) is cluster
            assert len(show_clusters()) == 1
            assert clusters[TEST_CLUSTER] == cluster

            try:
                save_environment(path=test_environment_file)
                with clear_environment():
                    assert show_clusters() == {}
                    load_environment(path=test_environment_file)
                    cluster2 = show_cluster(name=TEST_CLUSTER)
                    assert cluster2 is not cluster
                    assert cluster2 == cluster
            finally:
                os.remove(test_environment_file)
