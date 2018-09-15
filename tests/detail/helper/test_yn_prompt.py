import pytest
from fabric.context_managers import settings

from idact.detail.helper.yn_prompt import yn_prompt


def test_yn_prompt_default_yes_valid_inputs():
    with settings(prompts={'Prompt? [Y/n] ': 'y'}):
        assert yn_prompt('Prompt?')
    with settings(prompts={'Prompt? [Y/n] ': 'Y'}):
        assert yn_prompt('Prompt?')
    with settings(prompts={'Prompt? [Y/n] ': 'n'}):
        assert not yn_prompt('Prompt?')
    with settings(prompts={'Prompt? [Y/n] ': 'N'}):
        assert not yn_prompt('Prompt?')
    with settings(prompts={'Prompt? [Y/n] ': ''}):
        assert yn_prompt('Prompt?')


def test_yn_prompt_default_yes_invalid_inputs():
    with settings(prompts={'Prompt? [Y/n] ': 'y '}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?')
    with settings(prompts={'Prompt? [Y/n] ': ' n'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?')
    with settings(prompts={'Prompt? [Y/n] ': ' '}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?')
    with settings(prompts={'Prompt? [Y/n] ': 'yes'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?')
    with settings(prompts={'Prompt? [Y/n] ': 'Yes'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?')
    with settings(prompts={'Prompt? [Y/n] ': 'no'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?')
    with settings(prompts={'Prompt? [Y/n] ': 'No'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?')


def test_yn_prompt_default_no_valid_inputs():
    with settings(prompts={'Prompt? [y/N] ': 'y'}):
        assert yn_prompt('Prompt?', default=False)
    with settings(prompts={'Prompt? [y/N] ': 'Y'}):
        assert yn_prompt('Prompt?', default=False)
    with settings(prompts={'Prompt? [y/N] ': 'n'}):
        assert not yn_prompt('Prompt?', default=False)
    with settings(prompts={'Prompt? [y/N] ': 'N'}):
        assert not yn_prompt('Prompt?', default=False)
    with settings(prompts={'Prompt? [y/N] ': ''}):
        assert not yn_prompt('Prompt?', default=False)


def test_yn_prompt_default_no_invalid_inputs():
    with settings(prompts={'Prompt? [y/N] ': 'y '}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=False)
    with settings(prompts={'Prompt? [y/N] ': ' n'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=False)
    with settings(prompts={'Prompt? [y/N] ': ' '}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=False)
    with settings(prompts={'Prompt? [y/N] ': 'yes'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=False)
    with settings(prompts={'Prompt? [y/N] ': 'Yes'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=False)
    with settings(prompts={'Prompt? [y/N] ': 'no'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=False)
    with settings(prompts={'Prompt? [y/N] ': 'No'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=False)


def test_yn_prompt_no_default_valid_inputs():
    with settings(prompts={'Prompt? [y/n] ': 'y'}):
        assert yn_prompt('Prompt?', default=None)
    with settings(prompts={'Prompt? [y/n] ': 'Y'}):
        assert yn_prompt('Prompt?', default=None)
    with settings(prompts={'Prompt? [y/n] ': 'n'}):
        assert not yn_prompt('Prompt?', default=None)
    with settings(prompts={'Prompt? [y/n] ': 'N'}):
        assert not yn_prompt('Prompt?', default=None)


def test_yn_prompt_no_default_invalid_inputs():
    with settings(prompts={'Prompt? [y/n] ': ''}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=None)
    with settings(prompts={'Prompt? [y/n] ': 'y '}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=None)
    with settings(prompts={'Prompt? [y/n] ': ' n'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=None)
    with settings(prompts={'Prompt? [y/n] ': ' '}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=None)
    with settings(prompts={'Prompt? [y/n] ': 'yes'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=None)
    with settings(prompts={'Prompt? [y/n] ': 'Yes'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=None)
    with settings(prompts={'Prompt? [y/n] ': 'no'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=None)
    with settings(prompts={'Prompt? [y/n] ': 'No'}):
        with pytest.raises(RuntimeError):
            yn_prompt('Prompt?', default=None)
