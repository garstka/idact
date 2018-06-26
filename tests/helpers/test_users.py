"""User list for functional tests."""

USER_1 = 'user-1'
USER_2 = 'user-2'


def get_password(user: str) -> str:
    return user.replace('user-', 'pass-')
