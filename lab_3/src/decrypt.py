from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from src.utils import valid_cast5_key_length
from config.crypto_globals import PADDING 


def rsa_decrypt_content(private_key: RSAPrivateKey, encrypted_content: bytes) -> bytes:
    return private_key.decrypt(
        ciphertext=encrypted_content,
        padding=PADDING
    )


def rsa_decrypt_cast5_key(rsa_private_key: RSAPrivateKey, encrypted_cast5_key: bytes) -> bytes:
    cast5_key = rsa_decrypt_content(rsa_private_key, encrypted_cast5_key)
    
    bit_len = len(cast5_key) * 8
    valid_cast5_key_length(bit_len)

    return cast5_key
