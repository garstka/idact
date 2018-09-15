import os
import random
import re

from idact.core.auth import KeyType
from idact.detail.auth.generate_key import generate_key, RSA_BITS
from tests.helpers.set_up_key_location import set_up_key_location


def check_key_pair(host: str, path: str):
    """Checks the beginning and end of the private and public keys."""
    with open(path, 'r') as file:
        lines = file.read().splitlines()
    assert lines[0] == '-----BEGIN RSA PRIVATE KEY-----'
    assert lines[-1] == '-----END RSA PRIVATE KEY-----'
    assert len(lines) > 2

    with open(path + '.pub', 'r') as file:
        lines = file.read().splitlines()
    assert len(lines) == 1
    sections = lines[0].split(' ')
    assert len(sections) == 3
    assert sections[0] == 'ssh-rsa'
    assert re.match(
        pattern=r"idact/{host}/\d\d\d\d-\d\d-\d\dT\d\d:\d\d".format(
            host=host),
        string=sections[2])


def test_generate_key_when_location_is_free():
    """Key location is free."""
    random.seed(571303)

    assert RSA_BITS == 4096
    result_paths = []
    with set_up_key_location():
        for i in range(4):
            result_paths += [
                generate_key(host='host{}'.format(i),
                             key_type=KeyType.RSA)]

        expected_file_names = ['id_rsa_in',
                               'id_rsa_sy',
                               'id_rsa_ov',
                               'id_rsa_d9']
        expected_paths = [os.path.join(os.environ['IDACT_KEY_LOCATION'], i)
                          for i in expected_file_names]
        assert result_paths == expected_paths

        for i, path in enumerate(result_paths):
            check_key_pair(host="host{}".format(i),
                           path=path)


def test_generate_key_when_location_is_taken():
    """Key location is taken, must fall back."""
    random.seed(571303)
    with set_up_key_location():
        def get_expected_path(file_name: str) -> str:
            return os.path.join(os.environ['IDACT_KEY_LOCATION'], file_name)

        files_to_create = ['id_rsa_in',
                           'id_rsa_sy.pub',
                           'id_rsa_ov',
                           'id_rsa_ov.pub',
                           'id_rsa_d9']

        for file in files_to_create:
            with open(get_expected_path(file), 'w'):
                pass

        assert generate_key(host='host0', key_type=KeyType.RSA) == (
            get_expected_path('id_rsa_wg9o'))
        assert generate_key(host='host1', key_type=KeyType.RSA) == (
            get_expected_path('id_rsa_t1'))
        check_key_pair(host='host0',
                       path=get_expected_path('id_rsa_wg9o'))
        check_key_pair(host='host1',
                       path=get_expected_path('id_rsa_t1'))
