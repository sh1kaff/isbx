from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey

from config.crypto_globals import PADDING 


def rsa_encrypt_text(public_key: RSAPublicKey, text: bytes) -> bytes:
    return public_key.encrypt(
        text,
        PADDING
    )
