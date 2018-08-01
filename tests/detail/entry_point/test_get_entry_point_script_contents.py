from idact import AuthMethod
from idact.detail.config.client.client_cluster_config \
    import ClientClusterConfig
from idact.detail.entry_point.get_entry_point_script_contents import \
    get_entry_point_script_contents


def test_entry_point_disabled_sshd():
    config = ClientClusterConfig(host='host',
                                 port=123,
                                 user='user',
                                 auth=AuthMethod.PUBLIC_KEY,
                                 disable_sshd=True)
    formatted = get_entry_point_script_contents(config=config)
    assert formatted == ("#!/usr/bin/env bash\n"
                         "trap : TERM INT; sleep infinity & wait")


def test_entry_point_sshd():
    config = ClientClusterConfig(host='host',
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
                "mkdir -p ~/.idact/sshd_ports\n"
                "echo $(hostname):$SSHD_PORT"
                " >> ~/.idact/sshd_ports/alloc-$IDACT_ALLOCATION_ID\n"
                " $(which sshd)"
                " -D "
                " -f /dev/null"
                " -oListenAddress=0.0.0.0"
                " -oPort=$SSHD_PORT"
                " -oHostKey=~/.ssh/ssh_host_rsa_key"
                " -oPermitRootLogin=no"
                " -oStrictModes=yes"
                " -oPubkeyAuthentication=yes"
                " -oAuthorizedKeysFile=.ssh/authorized_keys.idact"
                " -oPasswordAuthentication=no"
                " -oChallengeResponseAuthentication=no"
                " -oKerberosAuthentication=no"
                " -oGSSAPIAuthentication=no"
                " -oUsePAM=no"
                " -oSubsystem='sftp /usr/libexec/openssh/sftp-server'"
                " -oX11Forwarding=yes\n"
                "exit $?")
    print()
    print(formatted)
    print(expected)
    assert formatted == expected
