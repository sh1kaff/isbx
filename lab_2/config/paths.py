import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(ROOT_DIR)


LANGS = [
    "cpp",
    "java"
]


EXEC_DIR = os.path.join(
    ROOT_DIR,
    "src",
    "gen",
    "execute"
)
