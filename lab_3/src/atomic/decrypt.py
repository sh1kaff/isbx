from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey
from cryptography.hazmat.decrepit.ciphers import algorithms
from cryptography.hazmat.primitives.ciphers import Cipher, modes

from src.utils import valid_cast5_key
from config.crypto_globals import RSA_PADDING, CAST5_PADDING


def rsa_decrypt_content(private_key: RSAPrivateKey, encrypted_content: bytes) -> bytes:
    return private_key.decrypt(
        ciphertext=encrypted_content,
        padding=RSA_PADDING
    )


def rsa_decrypt_cast5_key(rsa_private_key: RSAPrivateKey, encrypted_cast5_key: bytes) -> bytes:
    cast5_key = rsa_decrypt_content(rsa_private_key, encrypted_cast5_key)
    
    valid_cast5_key(cast5_key)

    return cast5_key


def cast5_decrypt_content(key: bytes, encrypted_padded_content: bytes) -> bytes:
    iv = encrypted_padded_content[:8]
    encrypted_padded_content = encrypted_padded_content[8:]

    cipher = Cipher(algorithms.CAST5(key), mode=modes.CBC(iv))
    decryptor = cipher.decryptor()
    unpadder = CAST5_PADDING.unpadder()

    padded_content = decryptor.update(encrypted_padded_content) + decryptor.finalize()
    content = unpadder.update(padded_content) + unpadder.finalize()

    return content
