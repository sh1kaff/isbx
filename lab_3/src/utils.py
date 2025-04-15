import base64
import json


def read_json(filepath: str) -> dict:
    with open(filepath, "r") as file:
        return json.load(file)


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


def valid_cast5_key(key: bytes):
    bit_len = len(key) * 8
    valid_cast5_key_length(bit_len)


def pem_headers(title: str) -> dict:
    return {
        "start": bytes(f"-----BEGIN {title}-----\n", encoding="UTF-8"),
        "end": bytes(f"-----END {title}-----\n", encoding="UTF-8")
    }


def serialize_content(content: bytes, title: str) -> bytes:
    headers = pem_headers(title)

    if isinstance(content, str):
        content = read_bytes(content)

    serialized_content = (
        headers["start"] +
        base64.encodebytes(content) +
        headers["end"]
    )

    return serialized_content


def deserialize_content(serialized_content: bytes, title: str) -> bytes:
    headers = pem_headers(title)

    if not serialized_content.startswith(headers["start"]) or not serialized_content.endswith(headers["end"]):
        raise ValueError("Unsupported file format")
    
    encoded_content = b"".join(serialized_content.split(b"\n")[1:-2])
    content = base64.decodebytes(encoded_content)

    return content
