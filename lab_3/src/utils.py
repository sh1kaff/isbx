import aiofiles
import json
import os

from config.messages import CRYPTO_ERRORS, COMMON_ERRORS


class AsyncIOUtils:
    @staticmethod
    async def async_write_bytes(filepath: str, content: bytes):
        if not os.path.isfile(filepath):
            raise ValueError(COMMON_ERRORS["not_file"].format(path=filepath))

        async with aiofiles.open(filepath, "wb") as file:
            await file.write(content)
    

    @staticmethod
    async def async_read_bytes(filepath: str) -> bytes:
        if not os.path.isfile(filepath):
            raise ValueError(COMMON_ERRORS["not_file"].format(path=filepath))

        async with aiofiles.open(filepath, "rb") as file:
            return await file.read()


class IOUtils:
    @staticmethod
    def read_json(filepath: str) -> dict:
        if not os.path.isfile(filepath):
                raise FileNotFoundError(COMMON_ERRORS["invalid_file_path"].format(path=filepath))

        if not filepath.endswith(".json"):
            raise ValueError(COMMON_ERRORS["file_not_json"].format(path=filepath))

        with open(filepath, "r") as file:
            return json.load(file)


    @staticmethod
    def write_bytes(filepath: str, content: bytes):
        if not os.path.isfile(filepath):
            raise ValueError(COMMON_ERRORS["not_file"].format(path=filepath)) 

        with open(filepath, "wb") as file:
            file.write(content)


    @staticmethod
    def read_bytes(filepath: str) -> bytes:
        if not os.path.isfile(filepath):
            raise ValueError(COMMON_ERRORS["not_file"].format(path=filepath))

        with open(filepath, "rb") as file:
            content = file.read()

        return content


class ValidCAST5Utils:
    @staticmethod
    def valid_cast5_key_length(bit_len: int):
        if bit_len < 40 or bit_len > 128:
            raise ValueError(CRYPTO_ERRORS["cast5_key_len"])

        if bit_len % 8 != 0:
            raise ValueError(CRYPTO_ERRORS["cast5_key_incr"])


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
