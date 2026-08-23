import sys
from pathlib import Path

from appdirs import AppDirs


class BaseAppInfo:
    NAME: str
    VERSION: str
    PUBLISHER: str
    ICON_PATH: str


class OPTIONS:
    APPLICATION_PATH = Path(sys.argv[0]).resolve().parent
    BASE_PATH = Path(sys.argv[0]).resolve().parent
    ICON_PATH: str = None

    theme = 'light'

    PORTABLE_SETTINGS_FILE = APPLICATION_PATH / 'settings.ini'
    PORTABLE_FLAG_PATH = APPLICATION_PATH / '.portable'
    portable = PORTABLE_FLAG_PATH.exists()

    config_dir: Path
    dirs: AppDirs

    app_info: BaseAppInfo
