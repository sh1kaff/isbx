from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from src.utils import valid_cast5_key
from config.crypto_globals import PADDING 


def rsa_encrypt_content(public_key: RSAPublicKey, content: bytes) -> bytes:
    return public_key.encrypt(
        plaintext=content,
        padding=PADDING
    )


def rsa_encrypt_cast5_key(public_key: RSAPublicKey, cast5_key: bytes) -> bytes:
    valid_cast5_key(cast5_key)

    encrypted_cast5_key = rsa_encrypt_content(public_key, cast5_key)

    return encrypted_cast5_key
