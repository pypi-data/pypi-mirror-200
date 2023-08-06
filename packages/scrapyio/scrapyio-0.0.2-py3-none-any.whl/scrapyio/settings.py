import typing
from types import ModuleType

from . import default_configs

LOADED = False

SETTINGS_FILE_NAME = "settings.py"
SETTINGS_FILE_NAME_FOR_IMPORT = "settings"

CONFIGS_TO_LOAD = ("MIDDLEWARES", "REQUEST_TIMEOUT")


def load_settings(path: typing.Optional[str] = None):
    global LOADED
    if LOADED:
        return
    custom_configs: typing.Union[ModuleType, object]
    try:
        custom_configs = __import__(path or SETTINGS_FILE_NAME_FOR_IMPORT)
    except ModuleNotFoundError:
        custom_configs = object()

    for attr in CONFIGS_TO_LOAD:
        value = getattr(custom_configs, attr, None)
        if value:
            setattr(default_configs, attr, value)
    LOADED = True
