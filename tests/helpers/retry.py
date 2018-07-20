from time import sleep


def retry(fun, retries: int, seconds_between_retries: int):
    """Retries function call, if it throws an exception.

        :param fun:   Function to call.

        :param times: Times to call the function.

        :param seconds_between_retries: Time between calls.

    """
    for i in range(0, retries + 1):
        try:
            return fun()
        except Exception as e:  # pylint: disable=broad-except
            if i >= retries:
                raise e
            print("Exception: {e}, retry {retry}/{retries}."
                  .format(e=e,
                          retry=i + 1,
                          retries=retries))
            sleep(seconds_between_retries)
