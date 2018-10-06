"""This module contains the user list for functional tests,
    e.g. :attr:`.USER_1`, :attr:`.USER_2` etc.

    Each functional test should run as a separate user.
    A fixed number of users is created as part of the testing setup,
    see :mod:`.testing_setup.ssh_add_users`.

"""

USER_1 = 'user-1'
USER_2 = 'user-2'
USER_3 = 'user-3'
USER_4 = 'user-4'
USER_5 = 'user-5'
USER_6 = 'user-6'
USER_7 = 'user-7'
USER_8 = 'user-8'
USER_9 = 'user-9'
USER_10 = 'user-10'
USER_11 = 'user-11'
USER_12 = 'user-12'
USER_13 = 'user-13'
USER_14 = 'user-14'
USER_15 = 'user-15'
USER_16 = 'user-16'
USER_17 = 'user-17'
USER_18 = 'user-18'
USER_19 = 'user-19'
USER_20 = 'user-20'
USER_21 = 'user-21'
USER_22 = 'user-22'
USER_23 = 'user-23'
USER_24 = 'user-24'
USER_25 = 'user-25'
USER_26 = 'user-26'
USER_27 = 'user-27'
USER_28 = 'user-28'
USER_29 = 'user-29'
USER_30 = 'user-30'
USER_31 = 'user-31'
USER_32 = 'user-32'
USER_33 = 'user-33'
USER_34 = 'user-34'
USER_35 = 'user-35'
USER_36 = 'user-36'
USER_37 = 'user-37'
USER_38 = 'user-38'
USER_39 = 'user-39'
USER_40 = 'user-40'
USER_41 = 'user-41'
USER_42 = 'user-42'


def get_test_user_password(user: str) -> str:
    """Returns the user's password.

        User password for `user-1` is `pass-1`, etc.

        :param user: User, whose password should be returned.

    """
    return user.replace('user-', 'pass-')
