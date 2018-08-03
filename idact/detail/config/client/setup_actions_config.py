from typing import List, Optional

from idact.core.config import SetupActionsConfig
from idact.detail.config.validation.validate_setup_actions import \
    validate_setup_actions


class SetupActionsConfigImpl(SetupActionsConfig):
    """Commands to run before deployment.

        :param jupyter: See :meth:`.SetupActionsConfigImpl.jupyter`

    """

    def __init__(self, jupyter: Optional[List[str]] = None):
        if jupyter is None:
            jupyter = []

        self._jupyter = validate_setup_actions(jupyter, 'jupyter')

    @property
    def jupyter(self) -> List[str]:
        return self._jupyter

    @jupyter.setter
    def jupyter(self, value: List[str]):
        self._jupyter = validate_setup_actions(value, 'jupyter')

    def __eq__(self, other):
        return self.__dict__ == other.__dict__
