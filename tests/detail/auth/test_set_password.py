"""Tests for password cache."""

from idact.detail.auth.set_password import set_password, PasswordCache


def test_set_password():
    """Store password in cache."""
    password_previous = PasswordCache().password
    with set_password('abc'):
        assert PasswordCache().password == 'abc'
    assert PasswordCache().password is password_previous
