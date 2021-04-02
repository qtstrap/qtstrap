from .qt import *
from pathlib import Path


class BaseMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
            
        self.setObjectName("MainWindow")
        self.load_settings()

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)
        
    def save_settings(self):
        QSettings().setValue("mainwindow/geometry", self.saveGeometry())
        QSettings().setValue("mainwindow/state", self.saveState())

    def load_settings(self):
        if QSettings().value("mainwindow/geometry") is not None:
            self.restoreGeometry(QSettings().value("mainwindow/geometry"))
        if QSettings().value("mainwindow/state") is not None:
            self.restoreState(QSettings().value("mainwindow/state"))