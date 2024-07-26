from qtstrap import *
from .widgets import BaseToolbar
import qtawesome as qta


class SettingsMenu(QMenu):
    def addAction(self, *args, **kwargs):
        shortcut = kwargs.pop('shortcut', None)
        action = super().addAction(*args, **kwargs)
        if shortcut:
            action.setShortcut(shortcut)
        return action


class ThemeMenu(QMenu):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)
        self.setTitle('Theme')

        self.addAction('Light').triggered.connect(lambda: QApplication.instance().change_theme('light'))
        self.addAction('Dark').triggered.connect(lambda: QApplication.instance().change_theme('dark'))


class BaseMainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setObjectName('MainWindow')
        self.load_settings()

    def closeEvent(self, event):
        self.save_settings()
        super().closeEvent(event)

    def save_settings(self):
        QSettings().setValue('mainwindow/geometry', self.saveGeometry())
        QSettings().setValue('mainwindow/state', self.saveState())

    def load_settings(self):
        geometry = QSettings().value('mainwindow/geometry')
        if isinstance(geometry, QByteArray):
            self.restoreGeometry(geometry)

        state = QSettings().value('mainwindow/state')
        if isinstance(state, QByteArray):
            self.restoreState(state)

    def create_sidebar(self):
        self.sidebar = BaseToolbar(self, 'sidebar', location='left', size=40)

    def create_statusbar(self):
        self.statusbar = BaseToolbar(self, 'statusbar', location='bottom', size=30)

        icon = qta.icon('fa.gear', color='gray')
        self.settings_btn = QToolButton(self.statusbar, icon=icon)
        self.settings_menu = SettingsMenu()
        self.settings_btn.setMenu(self.settings_menu)
        self.settings_btn.setPopupMode(QToolButton.InstantPopup)

        self.statusbar.addWidget(self.settings_btn)
