import pytest

from idact.detail.deployment.get_deployment_command import \
    get_deployment_command


def test_single_quote_is_not_allowed():
    with pytest.raises(ValueError):
        get_deployment_command("'")
    with pytest.raises(ValueError):
        get_deployment_command("''")
    with pytest.raises(ValueError):
        get_deployment_command("echo 'ABC DEF'")


def test_single_ampersand_is_not_allowed():
    with pytest.raises(ValueError):
        get_deployment_command("&")
    with pytest.raises(ValueError):
        get_deployment_command("a&b")
    with pytest.raises(ValueError):
        get_deployment_command("a &b")
    with pytest.raises(ValueError):
        get_deployment_command("a & b")
    with pytest.raises(ValueError):
        get_deployment_command("a\t& b")
    with pytest.raises(ValueError):
        get_deployment_command("ab &")


def test_negative_time_is_not_allowed():
    with pytest.raises(ValueError):
        get_deployment_command("echo abc",
                               capture_output_seconds=-1)
    with pytest.raises(ValueError):
        get_deployment_command("echo abc",
                               capture_output_seconds=-123)


def test_get_deployment_command():
    assert get_deployment_command("echo A B && rm \"ABC DEF\"") == (
        "exec 3< <(nohup bash -c"
        " 'sleep 1;''echo A B && rm \"ABC DEF\"' 2>&1)"
        " ; echo $!"
        " ; timeout 2 cat <&3"
        " ; exit 0")
    assert \
        get_deployment_command("echo \"A B\" \"C D\" || rm \"ABC DEF\"") == (
            "exec 3< <(nohup bash -c"
            " 'sleep 1;''echo \"A B\" \"C D\" || rm \"ABC DEF\"' 2>&1)"
            " ; echo $!"
            " ; timeout 2 cat <&3"
            " ; exit 0")
    assert get_deployment_command("echo \"A B\"; echo \"C D\";") == (
        "exec 3< <(nohup bash -c"
        " 'sleep 1;''echo \"A B\"; echo \"C D\";' 2>&1)"
        " ; echo $!"
        " ; timeout 2 cat <&3"
        " ; exit 0")
    assert get_deployment_command("echo A B > c.d") == (
        "exec 3< <(nohup bash -c"
        " 'sleep 1;''echo A B > c.d' 2>&1)"
        " ; echo $!"
        " ; timeout 2 cat <&3"
        " ; exit 0")
    assert \
        get_deployment_command("echo A B > c.d", capture_output_seconds=0) == (
            "exec 3< <(nohup bash -c"
            " 'sleep 1;''echo A B > c.d' 2>&1)"
            " ; echo $!"
            " ; timeout 1 cat <&3"
            " ; exit 0")
    assert \
        get_deployment_command("echo A B > c.d", capture_output_seconds=2) == (
            "exec 3< <(nohup bash -c"
            " 'sleep 1;''echo A B > c.d' 2>&1)"
            " ; echo $!"
            " ; timeout 3 cat <&3"
            " ; exit 0")
