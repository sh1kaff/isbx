from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from src.utils import read_bytes, write_bytes


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
