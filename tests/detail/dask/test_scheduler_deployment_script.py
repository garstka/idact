from idact.core.auth import AuthMethod
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.config.client.setup_actions_config import \
    SetupActionsConfigImpl
from idact.detail.dask.get_scheduler_deployment_script import \
    get_scheduler_deployment_script


def test_worker_deployment_script():
    config = ClusterConfigImpl(
        host='host',
        port=1234,
        user='user',
        auth=AuthMethod.ASK,
        setup_actions=SetupActionsConfigImpl(dask=['echo ABC',
                                                   'echo DEF']))
    script = get_scheduler_deployment_script(
        remote_port=1111,
        bokeh_port=2222,
        scratch_subdir='/scratch',
        log_file='/home/user/log',
        config=config)
    expected = (
        '#!/usr/bin/env bash\n'
        'echo ABC\n'
        'echo DEF\n'
        'export PATH="$PATH:$(python -m site --user-base)/bin"\n'
        'dask-scheduler --host 0.0.0.0 --port 1111 --bokeh --bokeh-port 2222'
        ' --no-show --local-directory /scratch'
        ' > /home/user/log 2>&1\n'
        'exit $?')
    print()
    print(repr(script))
    print(repr(expected))
    assert script == expected
