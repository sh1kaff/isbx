from src.generate import gen_rsa_keys_pair
from src.serialize import serialize_rsa_private_key
from src.encrypt import rsa_encrypt_text
from src.decrypt import rsa_decrypt_text

def main():
    pair = gen_rsa_keys_pair()

    text = bytes("hello man", encoding="UTF-8")

    e = rsa_encrypt_text(pair["public"], text)
    d = rsa_decrypt_text(pair["private"], e)
    print(e, "\n", d)
    # serialize_rsa_private_key(pair["private"], "test/asd.pem")


if __name__ == "__main__":
    main()