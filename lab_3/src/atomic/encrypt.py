from secrets import token_bytes
from cryptography.hazmat.decrepit.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher, modes
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from src.utils import valid_cast5_key
from config.crypto_globals import RSA_PADDING, CAST5_PADDING


def rsa_encrypt_content(public_key: RSAPublicKey, content: bytes) -> bytes:
    return public_key.encrypt(
        plaintext=content,
        padding=RSA_PADDING
    )


def rsa_encrypt_cast5_key(public_key: RSAPublicKey, cast5_key: bytes) -> bytes:
    valid_cast5_key(cast5_key)

    encrypted_cast5_key = rsa_encrypt_content(public_key, cast5_key)

    return encrypted_cast5_key


def cast5_encrypt_content(key: bytes, content: bytes) -> bytes:
    iv = token_bytes(8)

    cipher = Cipher(algorithms.CAST5(key), mode=modes.CBC(iv))
    encryptor = cipher.encryptor()
    padder = CAST5_PADDING.padder()

    padded_content = padder.update(content) + padder.finalize()
    encrypted_padded_content = encryptor.update(padded_content) + encryptor.finalize()

    return iv + encrypted_padded_content
