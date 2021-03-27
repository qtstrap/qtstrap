from .qt import *
from pathlib import Path


class BaseMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        icon_path = 'resources/application.ico'
        if Path(icon_path).exists():
            self.setWindowIcon(QIcon(icon_path))
            
        self.setObjectName("MainWindow")
        self.load_settings()

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)
        
    def save_settings(self):
        QSettings().setValue("window_geometry", self.saveGeometry())
        QSettings().setValue("window_state", self.saveState())

    def load_settings(self):
        if QSettings().value("window_geometry") is not None:
            self.restoreGeometry(QSettings().value("window_geometry"))
        if QSettings().value("window_state") is not None:
            self.restoreState(QSettings().value("window_state"))