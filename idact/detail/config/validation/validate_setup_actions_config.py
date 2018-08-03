from idact.detail.config.client.setup_actions_config import SetupActionsConfig
from idact.detail.config.validation.validation_error_message import \
    validation_error_message

VALID_SETUP_ACTIONS_CONFIG_DESCRIPTION = 'Instance of SetupActionsConfig.'


def validate_setup_actions_config(setup_actions) -> SetupActionsConfig:
    """Key path is optional, non-empty string.

        :param path: Object to validate.
    """

    if isinstance(setup_actions, SetupActionsConfig):
        return setup_actions

    raise TypeError(validation_error_message(
        label='setup_actions',
        value=setup_actions,
        expected=VALID_SETUP_ACTIONS_CONFIG_DESCRIPTION))
