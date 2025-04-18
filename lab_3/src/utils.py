import json
import aiofiles


def read_json(filepath: str) -> dict:
    with open(filepath, "r") as file:
        return json.load(file)


async def async_write_bytes(filepath: str, content: bytes):
    async with aiofiles.open(filepath, "wb") as file:
        await file.write(content)


def write_bytes(filepath: str, content: bytes):
    with open(filepath, "wb") as file:
        file.write(content)


async def async_read_bytes(filepath: str) -> bytes:
    async with aiofiles.open(filepath, "rb") as file:
        return await file.read()


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
