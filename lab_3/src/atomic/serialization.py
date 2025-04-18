import base64

from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKey, RSAPublicKey
from cryptography.hazmat.primitives import serialization

from src.utils import Utils
from config.crypto_consts import CAST5_ENCRYPTED_TITLE, CAST5_TITLE


class Serialization:
    @staticmethod
    def serialize_content(content: bytes, title: str) -> bytes:
        headers = Utils.pem_headers(title)

        if isinstance(content, str):
            content = Utils.read_bytes(content)

        serialized_content = (
            headers["start"] +
            base64.encodebytes(content) +
            headers["end"]
        )

        return serialized_content


    @staticmethod
    def deserialize_content(serialized_content: bytes, title: str) -> bytes:
        headers = Utils.pem_headers(title)

        if not serialized_content.startswith(headers["start"]) or not serialized_content.endswith(headers["end"]):
            raise ValueError("Unsupported file format")
        
        encoded_content = b"".join(serialized_content.split(b"\n")[1:-2])
        content = base64.decodebytes(encoded_content)

        return content


    @staticmethod
    def serialize_cast5_key(key: bytes) -> bytes:
        serialized_content = Serialization.serialize_content(
            key,
            CAST5_TITLE
        )

        return serialized_content


    @staticmethod
    def deserialize_cast5_key(serialized_key: bytes) -> bytes:
        encrypted_key = Serialization.deserialize_content(
            serialized_key,
            CAST5_TITLE
        )

        return encrypted_key


    @staticmethod
    def serialize_rsa_private_key(private_key: RSAPrivateKey) -> bytes:
        pem_content = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        return pem_content
    

    @staticmethod
    def serialize_rsa_public_key(public_key: RSAPublicKey) -> bytes:
        pem_content = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return pem_content

    @staticmethod
    def deserialize_rsa_private_key(
        pem_content: bytes,
        password: bytes | None = None
    ) -> RSAPrivateKey:
        private_key = serialization.load_pem_private_key(
            data=pem_content,
            password=password
        )

        return private_key


    @staticmethod
    def deserialize_rsa_public_key(pem_content: bytes) -> RSAPublicKey:
        public_key = serialization.load_pem_public_key(
            data=pem_content
        )

        return public_key


    @staticmethod
    def serialize_cast5_encrypted_key(encrypted_key: bytes) -> bytes:
        serialized_content = Serialization.serialize_content(
            encrypted_key,
            CAST5_ENCRYPTED_TITLE
        )

        return serialized_content
    

    @staticmethod
    def deserialize_cast5_encrypted_key(serialized_encrypted_key: bytes) -> bytes:
        encrypted_key = Serialization.deserialize_content(
            serialized_encrypted_key,
            CAST5_ENCRYPTED_TITLE
        )

        return encrypted_key
