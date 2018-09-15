"""This module contains a function for validating a setup actions config entry.
"""

from idact.detail.config.client.setup_actions_config import \
    SetupActionsConfigImpl
from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_SETUP_ACTIONS_CONFIG_DESCRIPTION = 'Instance of SetupActionsConfig.'


def validate_setup_actions_config(setup_actions) -> SetupActionsConfigImpl:
    """Returns the parameter, if it's a :class:`.SetupActionsConfigImpl`
        instance, otherwise raises an exception.

        :param setup_actions: Object to validate.

        :raises TypeError: On wrong type.

    """

    if isinstance(setup_actions, SetupActionsConfigImpl):
        return setup_actions

    raise TypeError(validation_error_message(
        label='setup_actions',
        value=setup_actions,
        expected=VALID_SETUP_ACTIONS_CONFIG_DESCRIPTION))
