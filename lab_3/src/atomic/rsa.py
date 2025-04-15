from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey

from src.utils import (
    read_bytes,
    write_bytes,
)
from config.crypto_consts import RSA_PADDING


class RSA:
    def __init__(self, private_key: RSAPrivateKey | None = None):
        if private_key is not None:
            self.private_key = private_key
            self.public_key = private_key.public_key()
            return

        key_pair = gen_rsa_key_pair()
        self.public_key = key_pair["public"]
        self.private_key = key_pair["private"]

    
    def import_private_key(self, filepath: str):
        self.private_key = RSA.deserialize("private", filepath)
        self.public_key = self.private_key.public_key()


    def encrypt(self, content: bytes) -> bytes:
        return rsa_encrypt_content(self.public_key, content)


    def decrypt(self, encrypted_content: bytes) -> bytes:
        return rsa_decrypt_content(self.private_key, encrypted_content)


    def serialize(self, key_type: str, filepath: str):
        match key_type:
            case "public":
                serialize_rsa_public_key(self.public_key, filepath)

            case "private":
                serialize_rsa_private_key(self.private_key, filepath)

            case _:
                raise ValueError(f"Unsupported key type: {key_type} (only 'public' or 'private')")


    @staticmethod
    def deserialize(key_type: str, filepath: str) -> RSAPrivateKey | RSAPublicKey:
        match key_type:
            case "public":
                return deserialize_rsa_public_key(filepath)

            case "private":
                return deserialize_rsa_private_key(filepath)

            case _:
                raise ValueError(f"Unsupported key type: {key_type} (only 'public' or 'private')")


def gen_rsa_key_pair(bit_len: int = 2048, public_exponent: int = 65537) -> dict[str, RSAPrivateKey | RSAPublicKey]:
    private_key = rsa.generate_private_key(
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
        padding=RSA_PADDING
    )


def rsa_decrypt_content(private_key: RSAPrivateKey, encrypted_content: bytes) -> bytes:
    return private_key.decrypt(
        ciphertext=encrypted_content,
        padding=RSA_PADDING
    )


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
