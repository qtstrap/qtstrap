from .qt import *


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
        if geometry := QSettings().value("mainwindow/geometry") is not None:
            self.restoreGeometry(geometry)
        if state := QSettings().value("mainwindow/state") is not None:
            self.restoreState(state)