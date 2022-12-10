from pathlib import Path
import sys
from appdirs import AppDirs


class OPTIONS:
    APPLICATION_PATH = Path(sys.argv[0]).parent.absolute()
    app_info_available = False
    app_info = None
    portable = False
    theme = 'light'
    PORTABLE_SETTINGS_FILE = Path(APPLICATION_PATH / 'settings.ini')
    PORTABLE_FLAG_PATH = Path(APPLICATION_PATH / '.portable')


# attempt to import app_info.py
try:
    import app_info

    OPTIONS.app_info_available = True
    OPTIONS.app_info = app_info
except ModuleNotFoundError:
    OPTIONS.app_info_available = False


# check for the file ".portable"
if Path(OPTIONS.PORTABLE_FLAG_PATH).exists():
    OPTIONS.portable = True


# set up appdirs
if not OPTIONS.portable and OPTIONS.app_info:
    dirs = AppDirs(app_info.AppName, app_info.AppPublisher)
    OPTIONS.config_dir = Path(dirs.user_config_dir)
    # Make sure the config directory exists
    Path(OPTIONS.config_dir).mkdir(parents=True, exist_ok=True)
else:
    if OPTIONS.PORTABLE_FLAG_PATH.is_dir():
        OPTIONS.config_dir = OPTIONS.PORTABLE_FLAG_PATH
    else:
        OPTIONS.config_dir = OPTIONS.PORTABLE_FLAG_PATH.parent
