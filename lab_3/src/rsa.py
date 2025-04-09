from cryptography.hazmat.primitives import serialization
import cryptography.hazmat.primitives.asymmetric as asymmetric
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey

from src.utils import (
    read_bytes,
    write_bytes,
    valid_cast5_key
)

from config.crypto_globals import PADDING 


def gen_rsa_key_pair(bit_len: int = 2048, public_exponent: int = 65537) -> dict:
    private_key = asymmetric.rsa.generate_private_key(
        key_size=bit_len,
        public_exponent=public_exponent
    )

    public_key = private_key.public_key()
    
    return {
        "public": public_key,
        "private": private_key
    }


def rsa_encrypt_content(public_key: RSAPublicKey, content: bytes) -> bytes:
    return public_key.encrypt(
        plaintext=content,
        padding=PADDING
    )


def rsa_encrypt_cast5_key(public_key: RSAPublicKey, cast5_key: bytes) -> bytes:
    valid_cast5_key(cast5_key)

    encrypted_cast5_key = rsa_encrypt_content(public_key, cast5_key)

    return encrypted_cast5_key


def rsa_decrypt_content(private_key: RSAPrivateKey, encrypted_content: bytes) -> bytes:
    return private_key.decrypt(
        ciphertext=encrypted_content,
        padding=PADDING
    )


def rsa_decrypt_cast5_key(rsa_private_key: RSAPrivateKey, encrypted_cast5_key: bytes) -> bytes:
    cast5_key = rsa_decrypt_content(rsa_private_key, encrypted_cast5_key)
    
    valid_cast5_key(cast5_key)

    return cast5_key


def serialize_rsa_private_key(private_key: RSAPrivateKey, filepath: str):
    pem_content = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    write_bytes(filepath, pem_content)


def deserialize_rsa_private_key(
    filepath: str,
    password: bytes | None = None
) -> RSAPrivateKey:
    pem_content = read_bytes(filepath)

    private_key = serialization.load_pem_private_key(
        data=pem_content,
        password=password
    )

    return private_key


def serialize_rsa_public_key(public_key: RSAPublicKey, filepath: str):
    pem_content = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    write_bytes(filepath, pem_content)


def deserialize_rsa_public_key(filepath: str) -> RSAPublicKey:
    pem_content = read_bytes(filepath)

    public_key = serialization.load_pem_public_key(
        data=pem_content
    )

    return public_key
