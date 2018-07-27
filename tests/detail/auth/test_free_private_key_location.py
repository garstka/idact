import os
import random

from typing import Optional

import pytest

from idact.core.auth import KeyType
from idact.detail.auth.get_free_private_key_location import \
    KEY_NAME_SUFFIX_LENGTH, get_key_suffix, KEY_NAME_SUFFIX_MAX_LENGTH, \
    get_key_path, try_generate_unique_path, get_free_private_key_location, \
    KEY_NAME_SUFFIX_RETRIES
from tests.helpers.set_up_key_location import set_up_key_location


def test_get_key_suffix():
    random.seed(571303)
    assert KEY_NAME_SUFFIX_LENGTH == 2
    assert get_key_suffix(2) == 'in'
    assert get_key_suffix(2) == 'sy'
    assert get_key_suffix(4) == 'ovd9'
    assert get_key_suffix(4) == 'wg9o'
    assert get_key_suffix(8) == 't14jdwud'
    assert get_key_suffix(8) == 'oa2v9tyb'
    assert get_key_suffix(16) == 'nbx2aspfb1npvy53'
    assert get_key_suffix(16) == '45nrc7gl4y4p3w95'
    assert get_key_suffix(32) == 'f8974vbce8uma56h9p6ez6e5p3pkvx3b'
    assert get_key_suffix(32) == 'q5hwplvbwzgo1ypfko2yz2vypimth8sq'
    assert KEY_NAME_SUFFIX_MAX_LENGTH == 32


def test_get_key_path():
    expected = ['/home/user/id_rsa_123',
                '/home/user\\id_rsa_123']
    assert get_key_path(location='/home/user',
                        prefix='id_rsa_',
                        suffix='123') in expected
    assert get_key_path(location='/home/user/',
                        prefix='id_rsa_',
                        suffix='123') in expected


def test_try_generate_unique_path_when_location_is_free():
    random.seed(571303)
    result_paths = []
    with set_up_key_location():
        for suffix_length in [2, 4, 8]:
            for _ in range(2):
                result_paths += [try_generate_unique_path(
                    suffix_length=suffix_length,
                    location=os.environ['IDACT_KEY_LOCATION'],
                    prefix='id_rsa_')]

    expected_file_names = ['id_rsa_in',
                           'id_rsa_sy',
                           'id_rsa_ovd9',
                           'id_rsa_wg9o',
                           'id_rsa_t14jdwud',
                           'id_rsa_oa2v9tyb']
    expected_paths = [os.path.join(os.environ['IDACT_KEY_LOCATION'],
                                   i) for i in expected_file_names]
    assert result_paths == expected_paths


def test_try_generate_unique_path_when_location_is_taken():
    with set_up_key_location():
        def try_generate() -> Optional[str]:
            return try_generate_unique_path(
                suffix_length=2,
                location=os.environ['IDACT_KEY_LOCATION'],
                prefix='id_rsa_')

        def get_expected_path(file_name: str) -> str:
            return os.path.join(os.environ['IDACT_KEY_LOCATION'], file_name)

        seed = 571303
        random.seed(seed)
        assert try_generate() == get_expected_path('id_rsa_in')
        assert try_generate() == get_expected_path('id_rsa_sy')

        random.seed(seed)
        assert try_generate() == get_expected_path('id_rsa_in')
        assert try_generate() == get_expected_path('id_rsa_sy')

        random.seed(seed)  # Private key already exists
        with open(get_expected_path('id_rsa_in'), 'w'):
            pass
        assert try_generate() is None
        assert try_generate() == get_expected_path('id_rsa_sy')
        os.remove(get_expected_path('id_rsa_in'))

        random.seed(seed)
        assert try_generate() == get_expected_path('id_rsa_in')
        assert try_generate() == get_expected_path('id_rsa_sy')

        random.seed(seed)  # Public key already exists
        with open(get_expected_path('id_rsa_in.pub'), 'w'):
            pass
        assert try_generate() is None
        assert try_generate() == get_expected_path('id_rsa_sy')
        os.remove(get_expected_path('id_rsa_in.pub'))


def test_get_free_private_key_location_when_location_is_free():
    random.seed(571303)
    result_paths = []
    with set_up_key_location():
        for _ in range(8):
            result_paths += [
                get_free_private_key_location(key_type=KeyType.RSA)]
    expected_file_names = ['id_rsa_in',
                           'id_rsa_sy',
                           'id_rsa_ov',
                           'id_rsa_d9',
                           'id_rsa_wg',
                           'id_rsa_9o',
                           'id_rsa_t1',
                           'id_rsa_4j']
    expected_paths = [os.path.join(os.environ['IDACT_KEY_LOCATION'], i)
                      for i in expected_file_names]
    assert result_paths == expected_paths


def test_get_free_private_key_location_when_location_is_taken():
    random.seed(571303)
    assert KEY_NAME_SUFFIX_RETRIES == 4
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

        def get_path():
            return get_free_private_key_location(key_type=KeyType.RSA)

        assert get_path() == get_expected_path('id_rsa_wg9o')
        assert get_path() == get_expected_path('id_rsa_t1')
        assert get_path() == get_expected_path('id_rsa_4j')


def test_get_free_private_key_location_when_all_locations_are_taken():
    random.seed(571303)

    with set_up_key_location():
        def get_expected_path(file_name: str) -> str:
            return os.path.join(os.environ['IDACT_KEY_LOCATION'], file_name)

        files_to_create = ['id_rsa_in',
                           'id_rsa_sy',
                           'id_rsa_ov',
                           'id_rsa_d9',
                           'id_rsa_wg9o',
                           'id_rsa_t14j',
                           'id_rsa_dwud',
                           'id_rsa_oa2v',
                           'id_rsa_9tybnbx2',
                           'id_rsa_aspfb1np',
                           'id_rsa_vy5345nr',
                           'id_rsa_c7gl4y4p',
                           'id_rsa_3w95f8974vbce8um',
                           'id_rsa_a56h9p6ez6e5p3pk',
                           'id_rsa_vx3bq5hwplvbwzgo',
                           'id_rsa_1ypfko2yz2vypimt',
                           'id_rsa_h8sqyu1avr7f5hwo3geil5nt8rkb9rx4',
                           'id_rsa_4xq0hw5qvhb9edcp9o2g5id1wmjbq1ro',
                           'id_rsa_f7c2epry1u1qzpac4hb7gymb3r3s3iex',
                           'id_rsa_im4sg2s7euj8j4h2no03qvhel4lcg9l1']

        for file in files_to_create:
            with open(get_expected_path(file), 'w'):
                pass

        with pytest.raises(RuntimeError):
            print(get_free_private_key_location(key_type=KeyType.RSA))
