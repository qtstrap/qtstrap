from qtstrap import OPTIONS
from .qt import *
import signal
from pathlib import Path


def install_ctrlc_handler(app):
    def ctrlc_handler(sig=None, frame=None):
        app.closeAllWindows() # this makes sure the MainWindow's .close() method gets called
        app.quit()
       
    # grab the keyboard interrupt signal 
    signal.signal(signal.SIGINT, ctrlc_handler)

    # empty timer callback
    def update():
        pass
    
    # create timer to force python interpreter to get some runtime
    app._ctrlc_timer = QTimer()
    app._ctrlc_timer.timeout.connect(update)
    app._ctrlc_timer.start(10)


def install_app_info(app):
    if OPTIONS.app_info:
        info = OPTIONS.app_info

        if info.AppPublisher:
            app.setOrganizationName(info.AppPublisher)
        if info.AppPublisher:
            app.setOrganizationDomain(info.AppPublisher)
        if info.AppName:
            app.setApplicationName(info.AppName)
        if info.AppVersion:
            app.setApplicationVersion(info.AppVersion)

        if files := list(Path(OPTIONS.APPLICATION_PATH).rglob(info.AppIconName)):
            app.setWindowIcon(QIcon(files[0].as_posix()))


class BaseApplication(QApplication):
    def __init__(self, *args, register_ctrlc_handler=True, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        install_app_info(self)

        if register_ctrlc_handler:
            install_ctrlc_handler(self)