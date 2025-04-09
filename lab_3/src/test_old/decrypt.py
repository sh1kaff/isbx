from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from src.utils import valid_cast5_key
from config.crypto_globals import PADDING 


def rsa_decrypt_content(private_key: RSAPrivateKey, encrypted_content: bytes) -> bytes:
    return private_key.decrypt(
        ciphertext=encrypted_content,
        padding=PADDING
    )


def rsa_decrypt_cast5_key(rsa_private_key: RSAPrivateKey, encrypted_cast5_key: bytes) -> bytes:
    cast5_key = rsa_decrypt_content(rsa_private_key, encrypted_cast5_key)
    
    valid_cast5_key(cast5_key)

    return cast5_key
