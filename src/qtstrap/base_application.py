import sys
from pathlib import Path
import inspect

import qtawesome as qta
from appdirs import AppDirs

from qtstrap import OPTIONS, BaseAppInfo
from qtstrap.extras.style import apply_theme

from .qt import *


class AppConfigError(Exception):
    """Error raised if the AppInfo hasn't been set"""

    def __init__(self):
        super().__init__("Configure your app's AppInfo")


class BaseApplication(QApplication):
    theme_changed = Signal()

    AppInfo: BaseAppInfo = None

    def __init__(self) -> None:
        super().__init__(sys.argv)

        if type(self) is not BaseApplication:
            OPTIONS.BASE_PATH = Path(inspect.getfile(type(self))).resolve().parent

        if self.AppInfo is None:
            raise AppConfigError

        info = self.AppInfo
        OPTIONS.app_info = info

        # set Qt app info
        self.setOrganizationName(info.PUBLISHER)
        self.setOrganizationDomain(info.PUBLISHER)
        self.setApplicationName(info.NAME)
        self.setApplicationVersion(info.VERSION)

        OPTIONS.ICON_PATH = (OPTIONS.BASE_PATH / info.ICON_PATH).as_posix()
        self.setWindowIcon(QIcon(OPTIONS.ICON_PATH))

        OPTIONS.dirs = AppDirs(info.NAME, info.PUBLISHER)
        OPTIONS.config_dir = Path(OPTIONS.dirs.user_config_dir)

        if Path(OPTIONS.PORTABLE_FLAG_PATH).exists():
            OPTIONS.portable = True

            if OPTIONS.PORTABLE_FLAG_PATH.is_dir():
                OPTIONS.config_dir = OPTIONS.PORTABLE_FLAG_PATH
            else:
                OPTIONS.config_dir = OPTIONS.PORTABLE_FLAG_PATH.parent

        Path(OPTIONS.config_dir).mkdir(parents=True, exist_ok=True)

        default_theme = 'light'
        theme = QSettings().value('theme', default_theme)
        self.change_theme(theme)

    def change_theme(self, theme: str, force=False):
        if not force and theme == OPTIONS.theme:
            return

        OPTIONS.theme = theme
        QSettings().setValue('theme', theme)

        # TODO: find and redraw all icons
        qta.reset_cache()
        apply_theme(theme, self)

        self.theme_changed.emit()
