import base64
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey


from src.atomic.rsa import rsa_encrypt_content, rsa_decrypt_content
from src.atomic.rsa import RSA
from src.atomic.cast5 import CAST5
from src.utils import (
    read_bytes,
    write_bytes,
    valid_cast5_key
)
from config.crypto_globals import CAST5_ENCRYPTED_SERIALIZATION_HEADERS


class HybridCryptoSystem:
    def __init__(
        self,
        cast5: CAST5 | None = None,
        rsa: RSA | None = None
    ):
        self.cast5 = cast5 or CAST5()
        self.rsa = rsa or RSA() 


    def encrypt_cast5_key(self) -> bytes:
        return rsa_encrypt_cast5_key(self.rsa.public_key, self.cast5.key)
    

    def decrypt_cast5_key(self, encrypted_cast5_key: bytes) -> bytes:
        return rsa_decrypt_cast5_key(self.rsa.rsa_private_key, encrypted_cast5_key)


    def serialize_cast5_encrypted_key(self, filepath: str):
        cast5_encrypted_key = self.encrypt_cast5_key() 
        serialize_cast5_encrypted_key(cast5_encrypted_key, filepath)
    

    def deserialize_cast5_encrypted_key(self, filepath: str) -> bytes:
        return deserialize_cast5_encrypted_key(filepath)


def rsa_encrypt_cast5_key(public_key: RSAPublicKey, cast5_key: bytes) -> bytes:
    valid_cast5_key(cast5_key)

    encrypted_cast5_key = rsa_encrypt_content(public_key, cast5_key)

    return encrypted_cast5_key


def rsa_decrypt_cast5_key(rsa_private_key: RSAPrivateKey, encrypted_cast5_key: bytes) -> bytes:
    cast5_key = rsa_decrypt_content(rsa_private_key, encrypted_cast5_key)
    
    valid_cast5_key(cast5_key)

    return cast5_key


def serialize_cast5_encrypted_key(encrypted_key: bytes, filepath: str):
    headers = CAST5_ENCRYPTED_SERIALIZATION_HEADERS

    content = (
        headers["start"] +
        base64.encodebytes(encrypted_key) +
        headers["end"]
    )

    write_bytes(filepath, content)


def deserialize_cast5_encrypted_key(filepath: str) -> bytes:
    headers = CAST5_ENCRYPTED_SERIALIZATION_HEADERS

    content = read_bytes(filepath)

    if not content.startswith(headers["start"]) or not content.endswith(headers["end"]):
        raise ValueError("Unsupported file format")
    
    encoded_encrypted_key = b"".join(content.split(b"\n")[1:-2])
    encrypted_key = base64.decodebytes(encoded_encrypted_key)

    return encrypted_key
