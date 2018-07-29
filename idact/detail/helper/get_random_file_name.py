import random
import string


def get_random_file_name(length: int) -> str:
    """Returns a random file name.

        :param length: File name length.

    """
    return ''.join(random.choice(string.ascii_lowercase
                                 + string.digits
                                 + string.ascii_uppercase)
                   for _ in range(length))
