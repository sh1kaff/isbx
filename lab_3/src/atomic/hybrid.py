from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey

from src.atomic.cast5 import CAST5
from src.atomic.rsa import RSA

from src.atomic.rsa import rsa_encrypt_content, rsa_decrypt_content
from src.utils import (
    read_bytes,
    write_bytes,
    valid_cast5_key,
    serialize_content,
    deserialize_content
)

from config.crypto_consts import CAST5_ENCRYPTED_TITLE


class HybridCryptoSystem:
    def __init__(
        self,
        cast5: CAST5 | None = None,
        rsa: RSA | None = None,
        cast5_keylen: int = 128
    ):
        self.cast5 = cast5 or CAST5(key_bit_len=cast5_keylen)
        self.rsa = rsa or RSA() 


    def import_keys(
        self, 
        rsa_private_key_filepath: str, 
        cast5_encrypted_key_filepath: str
    ):
        self.rsa.import_private_key(rsa_private_key_filepath)
        
        cast5_encrypted_key = self.deserialize_cast5_encrypted_key(cast5_encrypted_key_filepath)
        cast5_key = self.decrypt_cast5_key(cast5_encrypted_key)
        
        self.cast5 = CAST5(key=cast5_key)


    def serialize_keys(
        self,
        rsa_private_key_filepath: str,
        rsa_public_key_filepath: str,
        cast5_encrypted_key_filepath: str
    ):
        self.serialize_cast5_encrypted_key(cast5_encrypted_key_filepath)
        self.rsa.serialize("private", rsa_private_key_filepath)
        self.rsa.serialize("public", rsa_public_key_filepath)


    def encrypt_content(
        self,
        content: bytes | str,
        output_filepath: str | None = None
    ) -> bytes:
        if isinstance(content, str):
            content = read_bytes(content)

        encrypted_content = self.cast5.encrypt(content)
        if output_filepath is not None:
            write_bytes(output_filepath, encrypted_content)

        return encrypted_content


    def decrypt_content(
        self,
        encrypted_content: bytes | str,
        output_filepath: str | None = None
    ) -> bytes:
        if isinstance(encrypted_content, str):
            encrypted_content = read_bytes(encrypted_content)

        content = self.cast5.decrypt(encrypted_content)
        if output_filepath is not None:
            write_bytes(output_filepath, content)

        return content


    def encrypt_cast5_key(self) -> bytes:
        return rsa_encrypt_cast5_key(self.rsa.public_key, self.cast5.key)
    

    def decrypt_cast5_key(self, cast5_encrypted_key: bytes) -> bytes:
        return rsa_decrypt_cast5_key(self.rsa.private_key, cast5_encrypted_key)


    def serialize_cast5_encrypted_key(self, filepath: str):
        cast5_encrypted_key = self.encrypt_cast5_key() 
        serialize_cast5_encrypted_key(cast5_encrypted_key, filepath)
    

    @staticmethod
    def deserialize_cast5_encrypted_key(filepath: str) -> bytes:
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
    serialized_content = serialize_content(
        encrypted_key,
        CAST5_ENCRYPTED_TITLE
    )

    write_bytes(filepath, serialized_content)


def deserialize_cast5_encrypted_key(filepath: str) -> bytes:
    serialized_content = read_bytes(filepath)
    content = deserialize_content(
        serialized_content,
        CAST5_ENCRYPTED_TITLE
    )

    return content
