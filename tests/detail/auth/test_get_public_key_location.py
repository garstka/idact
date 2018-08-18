from idact.detail.auth.get_public_key_location import get_public_key_location


def test_get_public_key_location():
    """Public key location from private key location."""
    assert get_public_key_location('id_rsa') == 'id_rsa.pub'
    assert get_public_key_location('/home/user/.ssh/id_rsa_123') == (
        '/home/user/.ssh/id_rsa_123.pub')
