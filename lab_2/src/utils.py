import os
import subprocess

from config import config
from config.messages import ERRORS, NAMES


def valid_bits(bits: str):
    if len(bits) == 0:
        raise ValueError(ERRORS["empty_bit_string"])

    if not all(c in "01" for c in bits):
        raise ValueError(ERRORS["invalid_char_in_bits"])


def _execute(path: str) -> str:
    if not os.path.exists(path):
        raise ValueError(ERRORS["invalid_path"])

    output = subprocess.run(path, capture_output=True, text=True)
    return output.stdout


def get_exec_path(lang: str) -> str:
    if lang not in config.LANGS:
        raise ValueError(ERRORS["invalid_lang"])

    path = os.path.join(config.EXEC_DIR, NAMES["exe_file_name"].format(lang=lang))

    return path


def get_bits(lang: str) -> str:
    path = get_exec_path(lang)

    return _execute(path)

