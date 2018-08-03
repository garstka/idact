"""User list for functional tests."""

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


def get_test_user_password(user: str) -> str:
    return user.replace('user-', 'pass-')
