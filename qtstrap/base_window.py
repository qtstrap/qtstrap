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
        geometry = QSettings().value("mainwindow/geometry")
        if isinstance(geometry, QByteArray):
            self.restoreGeometry(geometry)
        
        state = QSettings().value("mainwindow/state")
        if isinstance(state, QByteArray):
            self.restoreState(state)