"""This module contains a function for displaying a yes/no prompt."""

import re
from typing import Optional

from fabric.state import env

VALIDATE_DEFAULT = re.compile(r'^([yYnN]|)$')

VALIDATE_NO_DEFAULT = re.compile(r'^[yYnN]$')


def yn_prompt(text: str, default: Optional[bool] = True) -> bool:
    """Asks the user a yes/no question.

        Returns `True` if the answer was `y`/`Y`, or `False` if the answer
        was `n`/`N`.
        Reprints prompt on invalid answer.
        Accepts automatic answers from Fabric's :attr:`.env.prompts`.

        :param text: Prompt value.

        :param default: Default value: can be `True` (yes), `False` (no),
                        or `None` (user must choose explicitly).

    """
    prompt_suffix = {True: ' [Y/n] ',
                     False: ' [y/N] ',
                     None: ' [y/n] '}
    result = {'y': True,
              'Y': True,
              'n': False,
              'N': False,
              '': default}
    prompt = text + prompt_suffix[default]
    validate = VALIDATE_DEFAULT if default is not None else VALIDATE_NO_DEFAULT
    if prompt in env.prompts:
        print(prompt, end='')
        auto_answer = env.prompts[prompt]
        if not validate.match(auto_answer):
            raise RuntimeError("Automatic prompt answer is invalid for"
                               " a yes/no prompt: '{}'.".format(auto_answer))
        print(auto_answer)
        prompt_input = auto_answer
    else:
        while True:
            print(prompt, end='')
            try:
                answer = input()
            except EOFError as e:
                raise IOError() from e

            if validate.match(answer):
                prompt_input = answer
                break

    return result[prompt_input]
