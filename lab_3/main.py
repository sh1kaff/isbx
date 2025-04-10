from src.cast5 import CAST5
from src.rsa import RSA


def main():
    cipher = RSA()
    
    data = b"hello man"
    c_d = cipher.encrypt(data)
    d_d = cipher.decrypt(c_d)

    print(c_d, "\n", d_d, sep="")

if __name__ == "__main__":
    main()
