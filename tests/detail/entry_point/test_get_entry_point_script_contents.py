from idact import AuthMethod
from idact.detail.config.client.client_cluster_config \
    import ClusterConfigImpl
from idact.detail.entry_point.get_entry_point_script_contents import \
    get_entry_point_script_contents


def test_entry_point_disabled_sshd():
    config = ClusterConfigImpl(host='host',
                               port=123,
                               user='user',
                               auth=AuthMethod.PUBLIC_KEY,
                               disable_sshd=True)
    formatted = get_entry_point_script_contents(config=config)
    assert formatted == ("#!/usr/bin/env bash\n"
                         "trap : TERM INT; sleep infinity & wait")


def test_entry_point_sshd():
    config = ClusterConfigImpl(host='host',
                               port=123,
                               user='user',
                               auth=AuthMethod.PUBLIC_KEY,
                               disable_sshd=False)
    formatted = get_entry_point_script_contents(config=config)
    expected = ("#!/usr/bin/env bash\n"
                "SSHD_PORT=$(python -c 'import socket;"
                " s=socket.socket();"
                " s.bind((str(), 0)); print(s.getsockname()[1]);"
                " s.close()')\n"
                "mkdir -p ~/.idact/sshd_ports/alloc-$IDACT_ALLOCATION_ID\n"
                "chmod 700 ~/.idact/sshd_ports/alloc-$IDACT_ALLOCATION_ID\n"
                "touch ~/.idact/sshd_ports/alloc-$IDACT_ALLOCATION_ID/$(hostname):$SSHD_PORT\n"  # noqa, pylint: disable=line-too-long
                "export PATH=\"$PATH:/usr/sbin\"\n"
                " $(which sshd)"
                " -D "
                " -f /dev/null"
                " -oPort=$SSHD_PORT"
                " -oListenAddress=0.0.0.0"
                " -oHostKey=~/.ssh/ssh_host_rsa_key"
                " -oProtocol=2"
                " -oAllowUsers=$USER"
                " -oPermitRootLogin=no"
                " -oStrictModes=yes"
                " -oPubkeyAuthentication=yes"
                " -oAuthorizedKeysFile=.ssh/authorized_keys.idact"
                " -oPasswordAuthentication=no"
                " -oChallengeResponseAuthentication=no"
                " -oKerberosAuthentication=no"
                " -oGSSAPIAuthentication=no"
                " -oUsePAM=no"
                " -oSubsystem='sftp internal-sftp'"
                " -oX11Forwarding=yes\n"
                "exit $?")
    assert formatted == expected
