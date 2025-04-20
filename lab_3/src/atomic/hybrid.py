from cryptography.hazmat.primitives.asymmetric.rsa import (
    RSAPublicKey,
    RSAPrivateKey
)

from src.atomic.cast5 import CAST5
from src.atomic.rsa import RSA

from src.atomic.rsa import rsa_encrypt_content, rsa_decrypt_content
from src.atomic.serialization import Serialization
from src.utils import Utils


class HybridCryptoSystem:
    def __init__(
        self,
        cast5: CAST5 | None = None,
        rsa: RSA | None = None,
        cast5_keylen: int = 128
    ):
        self.cast5 = cast5 or CAST5(key_bit_len=cast5_keylen)
        self.rsa = rsa or RSA()

    def import_keys_from_files(
        self,
        rsa_private_key_filepath: str,
        cast5_encrypted_key_filepath: str
    ):
        """Imports keys from files

        Args:
            rsa_private_key_filepath (str): Path to Private RSA Key
            cast5_encrypted_key_filepath (str): Path to the CAST5 encrypted key
        """
        ser_rsa_priv = Utils.read_bytes(rsa_private_key_filepath)
        self.rsa = RSA(
            private_key=Serialization.deserialize_rsa_private_key(ser_rsa_priv)
        )

        ser_cast5_enc_key = Utils.read_bytes(cast5_encrypted_key_filepath)
        cast5_encrypted_key = Serialization.deserialize_cast5_encrypted_key(
            ser_cast5_enc_key
        )
        cast5_key = rsa_decrypt_cast5_key(
            self.rsa.private_key,
            cast5_encrypted_key
        )

        self.cast5 = CAST5(key=cast5_key)

    def serialize_keys_to_files(
        self,
        rsa_private_key_filepath: str,
        rsa_public_key_filepath: str,
        cast5_encrypted_key_filepath: str
    ):
        """Serialization of keys to files

        Args:
            rsa_private_key_filepath (str): Path to RSA private key
            rsa_public_key_filepath (str): Path to RSA public key
            cast5_encrypted_key_filepath (str): Path to CAST5 enc key
        """
        ser_cast5_enc_key = Serialization.serialize_cast5_encrypted_key(
            rsa_encrypt_cast5_key(self.rsa.public_key, self.cast5.key)
        )
        ser_rsa_priv = self.rsa.serialize("private")
        ser_rsa_pub = self.rsa.serialize("public")

        Utils.write_bytes(rsa_private_key_filepath, ser_rsa_priv)
        Utils.write_bytes(rsa_public_key_filepath, ser_rsa_pub)
        Utils.write_bytes(cast5_encrypted_key_filepath, ser_cast5_enc_key)

    def encrypt_content(
        self,
        content: bytes | str,
        output_filepath: str | None = None
    ) -> bytes:
        """Content encryption

        Args:
            content (bytes | str): Content to encrypt
            output_filepath (str | None, optional): Save path. Defaults to None.

        Returns:
            bytes: Encrypted content
        """
        if isinstance(content, str):
            content = Utils.read_bytes(content)

        encrypted_content = self.cast5.encrypt(content)
        if output_filepath is not None:
            Utils.write_bytes(output_filepath, encrypted_content)

        return encrypted_content

    def decrypt_content(
        self,
        encrypted_content: bytes | str,
        output_filepath: str | None = None
    ) -> bytes:
        """Content decryption

        Args:
            encrypted_content (bytes | str): Encrypted content
            output_filepath (str | None, optional): Save path. Defaults to None.

        Returns:
            bytes: Original content
        """
        if isinstance(encrypted_content, str):
            encrypted_content = Utils.read_bytes(encrypted_content)

        content = self.cast5.decrypt(encrypted_content)
        if output_filepath is not None:
            Utils.write_bytes(output_filepath, content)

        return content


def rsa_encrypt_cast5_key(public_key: RSAPublicKey, cast5_key: bytes) -> bytes:
    """CAST5 key encryption 

    Args:
        public_key (RSAPublicKey): RSA public key
        cast5_key (bytes): CAST5 key

    Returns:
        bytes: Encrypted CAST5 key
    """
    Utils.valid_cast5_key(cast5_key)

    encrypted_cast5_key = rsa_encrypt_content(public_key, cast5_key)

    return encrypted_cast5_key


def rsa_decrypt_cast5_key(
    rsa_private_key: RSAPrivateKey,
    encrypted_cast5_key: bytes
) -> bytes:
    """CAST5 key decryption

    Args:
        rsa_private_key (RSAPrivateKey): RSA private key
        encrypted_cast5_key (bytes): Encrypted CAST5 key

    Returns:
        bytes: Decrypted CAST5 key
    """
    cast5_key = rsa_decrypt_content(rsa_private_key, encrypted_cast5_key)

    Utils.valid_cast5_key(cast5_key)

    return cast5_key
