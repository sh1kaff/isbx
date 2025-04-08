def write_bytes(filepath: str, content: bytes):
    with open(filepath, "wb") as file:
        file.write(content)


def read_bytes(filepath: str) -> bytes:
    with open(filepath, "rb") as file:
        content = file.read()

    return content