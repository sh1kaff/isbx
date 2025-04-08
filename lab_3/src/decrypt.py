from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey

from config.crypto_globals import PADDING 


def rsa_decrypt_text(private_key: RSAPrivateKey, encrypted_text: bytes) -> bytes:
    return private_key.decrypt(
        encrypted_text,
        PADDING
    )
