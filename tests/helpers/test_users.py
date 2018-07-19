"""User list for functional tests."""

USER_1 = 'user-1'
USER_2 = 'user-2'
USER_3 = 'user-3'
USER_4 = 'user-4'
USER_5 = 'user-5'
USER_6 = 'user-6'
USER_7 = 'user-7'


def get_test_user_password(user: str) -> str:
    return user.replace('user-', 'pass-')
