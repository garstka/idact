from idact.detail.deployment.get_deployment_command import \
    get_deployment_command


def test_get_deployment_command():
    assert get_deployment_command(script_path="a.sh") == (
        "nohup bash a.sh > /dev/null 2>&1"
        " & echo $!")

    assert get_deployment_command(script_path="dir/some file") == (
        "nohup bash 'dir/some file' > /dev/null 2>&1"
        " & echo $!")
