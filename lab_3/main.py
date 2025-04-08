from src.generate import gen_rsa_key_pair
from src.serialize import deserialize_rsa_private_key, serialize_rsa_private_key
from src.encrypt import rsa_encrypt_text
from src.decrypt import rsa_decrypt_text

def main():
    pair = gen_rsa_key_pair()

    serialize_rsa_private_key(pair["private"], "test/asd.pem")
    a = deserialize_rsa_private_key("test/asd.pem")
    print(a)

if __name__ == "__main__":
    main()