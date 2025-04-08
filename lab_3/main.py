from src.generate import gen_rsa_key_pair, gen_cast5_key
from src.serialize import deserialize_rsa_private_key, serialize_rsa_private_key, serialize_cast5_encrypted_key, deserialize_cast5_encrypted_key
from src.encrypt import rsa_encrypt_text
from src.decrypt import rsa_decrypt_text

def main():
    cast5_key = gen_cast5_key(128)
    print(len(cast5_key) * 8)

    # serialize_cast5_encrypted_key(cast5_key, "test/cast5.txt")
    deserialize_cast5_encrypted_key("test/cast5.txt")

if __name__ == "__main__":
    main()