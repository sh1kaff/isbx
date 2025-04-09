from src.cast5 import CAST5


def main():
    cipher = CAST5(40)

    data = b"hello world"

    e_d = cipher.encrypt(data)
    d_d = cipher.decrypt(e_d)

    print(e_d, "\n", d_d, sep="")


if __name__ == "__main__":
    main()
