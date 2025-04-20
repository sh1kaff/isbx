from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPrivateKey,
    RSAPublicKey
)

from src.atomic.serialization import Serialization

from config.crypto_consts import RSA_PADDING
from config.messages import CRYPTO_ERRORS


class RSA:
    def __init__(self, private_key: RSAPrivateKey | None = None):
        if private_key is not None:
            self.__private_key = private_key
            self.__public_key = private_key.public_key()
            return

        key_pair = gen_rsa_key_pair()
        self.__public_key = key_pair["public"]
        self.__private_key = key_pair["private"]

    @property
    def public_key(self) -> RSAPublicKey:
        """Public key getter

        Returns:
            RSAPublicKey: RSA public key
        """
        return self.__public_key

    @property
    def private_key(self) -> RSAPrivateKey:
        """Private key getter

        Returns:
            RSAPrivateKey: RSA private key
        """
        return self.__private_key

    @private_key.setter
    def private_key(self, priv_key: RSAPrivateKey):
        """RSA private key setter

        Args:
            priv_key (RSAPrivateKey): RSA private key
        """
        self.__private_key = priv_key
        self.__public_key = priv_key.public_key()

    def encrypt(self, content: bytes) -> bytes:
        """Same with rsa_encrypt_content()"""
        return rsa_encrypt_content(self.public_key, content)

    def decrypt(self, encrypted_content: bytes) -> bytes:
        """Same with rsa_decrypt_content()"""
        return rsa_decrypt_content(self.private_key, encrypted_content)

    def serialize(self, key_type: str) -> bytes:
        """RSA keys serialization

        Args:
            key_type (str): Key type ("private" or "public")

        Raises:
            ValueError: Unsupported key type

        Returns:
            bytes: Serialized key
        """
        match key_type:
            case "public":
                return Serialization.serialize_rsa_public_key(self.public_key)

            case "private":
                return Serialization.serialize_rsa_private_key(
                    self.private_key
                )

            case _:
                raise ValueError(CRYPTO_ERRORS["unsupported_key"].format(key_type=key_type))

    @staticmethod
    def deserialize(
        key_type: str,
        content: bytes
    ) -> RSAPrivateKey | RSAPublicKey:
        """RSA keys deserialization

        Args:
            key_type (str): Key type ("private" or "public")

        Raises:
            ValueError: Unsupported key type

        Returns:
            bytes: Deserialized key
        """
        match key_type:
            case "public":
                return Serialization.deserialize_rsa_public_key(content)

            case "private":
                return Serialization.deserialize_rsa_private_key(content)

            case _:
                raise ValueError(CRYPTO_ERRORS["unsupported_key"].format(key_type=key_type))


def gen_rsa_key_pair(
    bit_len: int = 2048,
    public_exponent: int = 65537
) -> dict[str, RSAPrivateKey | RSAPublicKey]:
    """RSA key pait generation

    Args:
        bit_len (int, optional): Key len. Defaults to 2048.
        public_exponent (int, optional): Public exponent. Defaults to 65537.

    Returns:
        dict[str, RSAPrivateKey | RSAPublicKey]: Key pair
    """
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
    """Encryption content

    Args:
        public_key (RSAPublicKey): RSA public key
        content (bytes): Content to encryption

    Returns:
        bytes: Encrypted content
    """
    return public_key.encrypt(
        plaintext=content,
        padding=RSA_PADDING
    )


def rsa_decrypt_content(
    private_key: RSAPrivateKey,
    encrypted_content: bytes
) -> bytes:
    """Content decryption

    Args:
        private_key (RSAPrivateKey): RSA private key
        encrypted_content (bytes): Encrypted content

    Returns:
        bytes: Original content
    """
    try:
        return private_key.decrypt(
            ciphertext=encrypted_content,
            padding=RSA_PADDING
        )
    except:
        ValueError(CRYPTO_ERRORS["decrypt_invalid_rsa"])
