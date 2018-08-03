import pytest

from idact.detail.deployment.get_deployment_command import \
    get_deployment_command


def test_negative_time_is_not_allowed():
    with pytest.raises(ValueError):
        get_deployment_command("echo abc",
                               capture_output_seconds=-1)
    with pytest.raises(ValueError):
        get_deployment_command("echo abc",
                               capture_output_seconds=-123)


def test_get_deployment_command():
    assert get_deployment_command(script_path="a.sh") == (
        "exec 3< <(nohup bash -c"
        " 'sleep 1;'a.sh 2>&1)"
        " ; echo $!"
        " ; timeout 2 cat <&3"
        " ; rm -f a.sh"
        " ; exit 0")
    assert get_deployment_command(
        script_path="b.sh",
        capture_output_seconds=0) == ("exec 3< <(nohup bash -c"
                                      " 'sleep 1;'b.sh 2>&1)"
                                      " ; echo $!"
                                      " ; timeout 1 cat <&3"
                                      " ; rm -f b.sh"
                                      " ; exit 0")
    assert get_deployment_command(
        script_path="c.sh",
        capture_output_seconds=2) == ("exec 3< <(nohup bash -c"
                                      " 'sleep 1;'c.sh 2>&1)"
                                      " ; echo $!"
                                      " ; timeout 3 cat <&3"
                                      " ; rm -f c.sh"
                                      " ; exit 0")
    assert get_deployment_command(script_path="dir/some file") == (
        "exec 3< <(nohup bash -c"
        " 'sleep 1;''dir/some file' 2>&1)"
        " ; echo $!"
        " ; timeout 2 cat <&3"
        " ; rm -f 'dir/some file'"
        " ; exit 0")
