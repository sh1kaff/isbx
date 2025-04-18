import json
import aiofiles


class AsyncIOUtils:
    @staticmethod
    async def async_write_bytes(filepath: str, content: bytes):
        async with aiofiles.open(filepath, "wb") as file:
            await file.write(content)
    

    @staticmethod
    async def async_read_bytes(filepath: str) -> bytes:
        async with aiofiles.open(filepath, "rb") as file:
            return await file.read()


class IOUtils:
    @staticmethod
    def read_json(filepath: str) -> dict:
        with open(filepath, "r") as file:
            return json.load(file)


    @staticmethod
    def write_bytes(filepath: str, content: bytes):
        with open(filepath, "wb") as file:
            file.write(content)


    @staticmethod
    def read_bytes(filepath: str) -> bytes:
        with open(filepath, "rb") as file:
            content = file.read()

        return content


class ValidCAST5Utils:
    @staticmethod
    def valid_cast5_key_length(bit_len: int):
        if bit_len < 40 or bit_len > 128:
            raise ValueError("The key length must be between 40 and 128 bits inclusive")

        if bit_len % 8 != 0:
            raise ValueError("The key length should be in 8 bit increments")


    @staticmethod
    def valid_cast5_key(key: bytes):
        bit_len = len(key) * 8
        ValidCAST5Utils.valid_cast5_key_length(bit_len)


class OtherUtils:
    @staticmethod
    def pem_headers(title: str) -> dict:
        return {
            "start": bytes(f"-----BEGIN {title}-----\n", encoding="UTF-8"),
            "end": bytes(f"-----END {title}-----\n", encoding="UTF-8")
        }


class Utils(
    AsyncIOUtils,
    IOUtils,
    ValidCAST5Utils,
    OtherUtils
):
    pass