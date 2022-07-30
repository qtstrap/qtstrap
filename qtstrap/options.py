from pathlib import Path
import sys
from appdirs import AppDirs


class OPTIONS:
    APPLICATION_PATH = Path(sys.argv[0]).parent.absolute()
    app_info_available = False
    app_info = None
    portable = False
    PORTABLE_SETTINGS_FILE = Path(APPLICATION_PATH / 'settings.ini')
    PORTABLE_FLAG_FILE = Path(APPLICATION_PATH / '.portable')


# attempt to import app_info.py
try:
    import app_info

    OPTIONS.app_info_available = True
    OPTIONS.app_info = app_info
except ModuleNotFoundError:
    OPTIONS.app_info_available = False


# check for the file ".portable"
if Path(OPTIONS.PORTABLE_FLAG_FILE).exists():
    OPTIONS.portable = True


# set up appdirs
if not OPTIONS.portable and OPTIONS.app_info:
    dirs = AppDirs(app_info.AppName, app_info.AppPublisher)
    OPTIONS.config_dir = dirs.user_config_dir
else:
    OPTIONS.config_dir = OPTIONS.APPLICATION_PATH.as_posix()
