import pytest

from idact.detail.config.client.setup_actions_config import SetupActionsConfig


def test_setup_actions():
    setup_actions = SetupActionsConfig()
    assert setup_actions.jupyter == []
    setup_actions.jupyter = ['abcd']
    assert setup_actions.jupyter == ['abcd']
    with pytest.raises(TypeError):
        setup_actions.jupyter = 12
    assert setup_actions.jupyter == ['abcd']
    with pytest.raises(TypeError):
        setup_actions.jupyter = ['asdasd', 12]
