import binascii
from os import urandom as generate_bytes

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

from knox.settings import knox_settings

sha = knox_settings.SECURE_HASH_ALGORITHM


def create_token_string():
    return binascii.hexlify(
        generate_bytes(int(knox_settings.AUTH_TOKEN_CHARACTER_LENGTH / 2))
    ).decode()


def make_hex_compatible(token: str) -> str:
    """
    We need to make sure that the token, that is send is hex-compatible.
    When a token prefix is used, we cannot garantee that.
    """
    return binascii.unhexlify(binascii.hexlify(bytes(token, 'utf-8')))


def hash_token(token):
    '''
    Calculates the hash of a token.
    input is unhexlified

    token must contain an even number of hex digits or a binascii.Error
    exception will be raised
    '''
    digest = hashes.Hash(sha(), backend=default_backend())
    digest.update(binascii.unhexlify(token))
    return binascii.hexlify(digest.finalize()).decode()

