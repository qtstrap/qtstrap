import inspect
import signal
import socket
import sys
from pathlib import Path

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
    INSTALL_SIGNAL_HANDLERS = True

    def __init__(self) -> None:
        super().__init__(sys.argv)

        if self.INSTALL_SIGNAL_HANDLERS:
            self._install_signal_handlers()

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

    def _install_signal_handlers(self) -> None:
        """Make SIGINT (ctrl-c) and SIGTERM (logout, kill) quit gracefully.

        CPython only delivers Python-level signal handlers while bytecode is
        executing, and Qt's C event loop starves the interpreter. The C-level
        handler writes a byte to a socketpair; the QSocketNotifier wakes the
        Qt loop, and entering the Python callback is what lets the pending
        handler fire. No polling timer needed.

        Anything that installs its own handlers after this wins (last writer
        takes the signal) — e.g. QtAsyncio.run(handle_sigint=True) resets
        SIGINT to immediate death; pass handle_sigint=False.
        """
        self._signal_rsock, self._signal_wsock = socket.socketpair()
        self._signal_wsock.setblocking(False)
        signal.set_wakeup_fd(self._signal_wsock.fileno())

        self._signal_notifier = QSocketNotifier(self._signal_rsock.fileno(), QSocketNotifier.Type.Read, self)
        self._signal_notifier.activated.connect(lambda: self._signal_rsock.recv(512))

        def quit_on_signal(sig=None, frame=None):
            self.closeAllWindows()
            self.quit()

        signal.signal(signal.SIGINT, quit_on_signal)
        signal.signal(signal.SIGTERM, quit_on_signal)

    def change_theme(self, theme: str, force=False):
        if not force and theme == OPTIONS.theme:
            return

        OPTIONS.theme = theme
        QSettings().setValue('theme', theme)

        # TODO: find and redraw all icons
        qta.reset_cache()
        apply_theme(theme, self)

        self.theme_changed.emit()
