from idact.detail.auth.set_password import set_password, PasswordCache


def test_set_password():
    password_previous = PasswordCache().password
    with set_password('abc'):
        assert PasswordCache().password == 'abc'
    assert PasswordCache().password is password_previous
