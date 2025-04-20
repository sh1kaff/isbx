import os


ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(ROOT_DIR)


TMP_DIR = os.path.join(
    ROOT_DIR,
    "tmp"
)


TEMPLATES_DIR = os.path.join(
    ROOT_DIR,
    "templates"
)


STATIC_DIR = os.path.join(
    ROOT_DIR,
    "static"
)


DEFAULT_DIR = os.path.join(
    ROOT_DIR,
    "default"
)


CONFIG_DIR = os.path.join(
    ROOT_DIR,
    "config"
)


USER_SETTINGS_FILE = os.path.join(
    CONFIG_DIR,
    "user_settings.json"
)
