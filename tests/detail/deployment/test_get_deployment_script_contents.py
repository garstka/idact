from idact.detail.deployment.get_deployment_script_contents import \
    get_deployment_script_contents


def test_deployment_script_empty():
    formatted = get_deployment_script_contents(deployment_commands=[],
                                               setup_actions=[])

    expected = ("#!/usr/bin/env bash\n"
                "exit $?")
    assert formatted == expected


def test_deployment_script_only_deployment_commands():
    formatted = get_deployment_script_contents(
        deployment_commands=['echo a > b'],
        setup_actions=[])

    expected = ("#!/usr/bin/env bash\n"
                "echo a > b\n"
                "exit $?")
    assert formatted == expected


def test_deployment_script_one_each():
    formatted = get_deployment_script_contents(
        deployment_commands=['echo a > b'],
        setup_actions=['echo d'])

    expected = ("#!/usr/bin/env bash\n"
                "echo d\n"
                "echo a > b\n"
                "exit $?")
    assert formatted == expected


def test_deployment_script_multiple_both():
    formatted = get_deployment_script_contents(
        deployment_commands=['echo a > b',
                             'echo f'],
        setup_actions=['echo d',
                       'echo e'])

    expected = ("#!/usr/bin/env bash\n"
                "echo d\n"
                "echo e\n"
                "echo a > b\n"
                "echo f\n"
                "exit $?")
    assert formatted == expected


def test_deployment_script_no_validation():
    formatted = get_deployment_script_contents(
        deployment_commands=['AS*_aV#_$$!!QU_#QA(RUQ#"',
                             'exit 1'],
        setup_actions=[])

    expected = ("#!/usr/bin/env bash\n"
                "AS*_aV#_$$!!QU_#QA(RUQ#\"\n"
                "exit 1\n"
                "exit $?")
    assert formatted == expected
