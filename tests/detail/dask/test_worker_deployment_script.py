import bitmath

from idact import AuthMethod
from idact.detail.config.client.client_cluster_config import ClusterConfigImpl
from idact.detail.config.client.setup_actions_config import \
    SetupActionsConfigImpl
from idact.detail.dask.get_worker_deployment_script import \
    get_worker_deployment_script


def test_scheduler_deployment_script():
    config = ClusterConfigImpl(
        host='host',
        port=1234,
        user='user',
        auth=AuthMethod.ASK,
        setup_actions=SetupActionsConfigImpl(dask=['echo ABC',
                                                   'echo DEF']))
    script = get_worker_deployment_script(
        scheduler_address='tcp://localhost:1111/',
        bokeh_port=2222,
        scratch_subdir='/scratch',
        cores=12,
        memory_limit=bitmath.GiB(10),
        log_file='/home/user/log',
        config=config)
    expected = (
        '#!/usr/bin/env bash\n'
        'echo ABC\n'
        'echo DEF\n'
        'export PATH="$PATH:$(python -m site --user-base)/bin"\n'
        'dask-worker tcp://localhost:1111/ --host 0.0.0.0 --bokeh'
        ' --bokeh-port 2222 --nanny --reconnect --nprocs 1 --nthreads 12'
        ' --memory-limit 10737418240 --local-directory /scratch'
        ' > /home/user/log 2>&1\n'
        'exit $?')
    print()
    print(repr(script))
    print(repr(expected))
    assert script == expected
