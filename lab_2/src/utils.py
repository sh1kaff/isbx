import os
import subprocess

from config.config import EXEC_DIR, LANGS
from config.messages import ERRORS, NAMES


def valid_bits(bits: str):
    """Checks that the bit string is valid

    Args:
        bits (str): bits string

    Raises:
        ValueError: bits string is empty
        ValueError: bit string contains unresolved characters
    """
    if len(bits) == 0:
        raise ValueError(ERRORS["empty_bit_string"])

    if not all(c in "01" for c in bits):
        raise ValueError(ERRORS["invalid_char_in_bits"])


def _execute(path: str) -> str:
    """A function to execute a file (presumably .exe) on its path.
        This function is supposed to be private and should not be
        called anywhere other than this file

    Args:
        path (str): path to file

    Raises:
        ValueError: the path doesn't exist or it's wrong

    Returns:
        str: result of program execution
    """
    if not os.path.exists(path):
        raise ValueError(ERRORS["invalid_path"].format(path=path))

    output = subprocess.run(path, capture_output=True, text=True)
    return output.stdout


def get_exec_path(lang: str) -> str:
    """Gets the path to the executable file by language key

    Args:
        lang (str): lang key

    Raises:
        ValueError: incorrect language key

    Returns:
        str: path to executable
    """
    if lang not in LANGS:
        raise ValueError(ERRORS["invalid_lang"].format(lang=lang))

    path = os.path.join(
        EXEC_DIR, NAMES["exe_file_name"].format(lang=lang)
    )

    return path


def get_bits(lang: str) -> str:
    """Executes the file and returns the generated bits

    Args:
        lang (str): lang key

    Returns:
        str: bits string
    """
    path = get_exec_path(lang)

    return _execute(path)
