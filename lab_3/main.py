from src.generate import (
    gen_rsa_key_pair,
    gen_cast5_key
)
from src.serialize import (
    deserialize_rsa_private_key,
    serialize_rsa_private_key,
    serialize_cast5_encrypted_key,
    deserialize_cast5_encrypted_key
)
from src.encrypt import rsa_encrypt_content
from src.decrypt import rsa_decrypt_content, rsa_decrypt_cast5_key


def main():
    cast5_key = gen_cast5_key(128)
    rsa_pair = gen_rsa_key_pair()

    encrypted_cast5_key = rsa_encrypt_content(rsa_pair["public"], cast5_key)

    serialize_cast5_encrypted_key(encrypted_cast5_key, "test/cast5.txt")
    
    encrypted_cast5_key2 = deserialize_cast5_encrypted_key("test/cast5.txt")

    cast5_key2 = rsa_decrypt_cast5_key(rsa_pair["private"], encrypted_cast5_key2)

    print(cast5_key)
    print(cast5_key2)


if __name__ == "__main__":
    main()
