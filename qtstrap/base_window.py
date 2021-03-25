from .qt import *


class BaseMainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
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