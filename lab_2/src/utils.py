import os
import subprocess

import config.paths as paths


def valid_bits(bits: str):
    if len(bits) == 0:
        raise ValueError("Empty bits string")

    if not all(c in "01" for c in bits):
        raise ValueError("Bits contains invalid character")


def _execute(path: str) -> str:
    if not os.path.exists(path):
        raise ValueError("path do not exists")

    output = subprocess.run(path, capture_output=True, text=True)
    return output.stdout


def get_exec_path(lang: str) -> str:
    if lang not in paths.LANGS:
        raise ValueError("lang not valid")

    path = os.path.join(paths.EXEC_DIR, f"gen_{lang}.exe")

    return path


def get_bits(lang: str) -> str:
    path = get_exec_path(lang)

    return _execute(path)
