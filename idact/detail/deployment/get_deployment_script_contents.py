"""This module contains a function for generating a deployment script."""

from typing import List


def get_deployment_script_contents(deployment_commands: List[str],
                                   setup_actions: List[str]) -> str:
    """Formats a full deployment script and returns its contents.

        :param deployment_commands: Main actions for deployment.

        :param setup_actions: Setup actions from config.

    """

    setup_actions_str = ('\n'.join(setup_actions + [''])
                         if setup_actions
                         else '')
    deployment_commands_str = ('\n'.join(deployment_commands + [''])
                               if deployment_commands
                               else '')

    script_contents = \
        ("#!/usr/bin/env bash\n"
         "{setup_actions_str}"
         "{deployment_commands_str}"
         "exit $?").format(setup_actions_str=setup_actions_str,
                           deployment_commands_str=deployment_commands_str)

    return script_contents
