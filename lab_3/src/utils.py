def write_bytes(filepath: str, content: bytes):
    with open(filepath, "wb") as file:
        file.write(content)


def read_bytes(filepath: str) -> bytes:
    with open(filepath, "rb") as file:
        content = file.read()

    return content


def valid_cast5_key_length(bit_len: int):
    if bit_len < 40 or bit_len > 128:
        raise ValueError("The key length must be between 40 and 128 bits inclusive")

    if bit_len % 8 != 0:
        raise ValueError("The key length should be in 8 bit increments")
