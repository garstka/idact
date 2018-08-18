"""This module contains a function for generating random file names."""

import random
import string


def get_random_file_name(length: int) -> str:
    """Returns a random file name.

        File name consists of lowercase letters, uppercase letters, and digits.

        :param length: File name length.

    """
    return ''.join(random.choice(string.ascii_lowercase
                                 + string.digits
                                 + string.ascii_uppercase)
                   for _ in range(length))
