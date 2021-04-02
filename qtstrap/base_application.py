from qtstrap import OPTIONS
from .qt import *
import signal
from pathlib import Path
from appdirs import AppDirs


class BaseApplication(QApplication):
    organization_name = None
    organization_domain = None
    application_name = None
    application_version = None
    
    def __init__(self, *args, register_ctrlc_handler=True, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        if OPTIONS.app_info:
            self.init_app_info(OPTIONS.app_info)
            self.init_app_dirs(OPTIONS.app_info)
            self.init_app_icon(OPTIONS.app_info.AppIconName)

        if register_ctrlc_handler:
            self.init_ctrlc_handler()

    def ctrlc_handler(self, sig=None, frame=None):
        # give all the app's children a chance to close
        for child in self.children():
            if hasattr(child, 'close'):
                child.close()

        # TODO: should we somehow wait for our children to close?

        # tell the application to close
        self.shutdown()

    def init_ctrlc_handler(self):            
        # grab the keyboard interrupt signal 
        signal.signal(signal.SIGINT, self.ctrlc_handler)

        # empty timer callback
        def update():
            pass
        
        # create timer to force python interpreter to get some runtime
        self.timer = QTimer()
        self.timer.timeout.connect(update)
        self.timer.start(10)
    
    def init_app_info(self, info):
        if info.AppPublisher:
            self.organization_name = info.AppPublisher
            self.setOrganizationName(info.AppPublisher)
        if info.AppPublisher:
            self.organization_domain = info.AppPublisher
            self.setOrganizationDomain(info.AppPublisher)
        if info.AppName:
            self.application_name = info.AppName
            self.setApplicationName(info.AppName)
        if info.AppVersion:
            self.application_version = info.AppVersion
            self.setApplicationVersion(info.AppVersion)

    def init_app_icon(self, icon_path):
        if icon_path and Path(icon_path).exists():
                self.setWindowIcon(QIcon(icon_path))

    def init_app_dirs(self, info):
        if not OPTIONS.portable:
            self.dirs = AppDirs(info.AppName, info.AppPublisher)
            self.config_dir = self.dirs.user_config_dir

            # make sure config dir exists
            Path(self.config_dir).mkdir(parents=True, exist_ok=True)
        else:
            self.config_dir = OPTIONS.APPLICATION_PATH