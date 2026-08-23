from qtstrap import *
import pytest


class AppInfo(BaseAppInfo):
    NAME = 'test-app'
    VERSION = '0.0.0'
    PUBLISHER = 'test'
    ICON_PATH = ''


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.button = QPushButton('Click me!', clicked=lambda: self.label.setText('clicked'))
        self.label = QLabel('^^^^^^^')

        with CVBoxLayout(self) as layout:
            layout.add(self.button)
            layout.add(self.label)


class Application(BaseApplication):
    AppInfo = AppInfo

    def __init__(self) -> None:
        super().__init__()

        self.window = MainWindow()


@pytest.fixture(scope="session")
def qapp():
    yield Application()


def test_base_application_startup(qtbot, qapp):
    qtbot.addWidget(qapp.window)
    assert qapp.window.label.text() == '^^^^^^^'

    qtbot.mouseClick(qapp.window.button, QtCore.Qt.LeftButton)
    assert qapp.window.label.text() == 'clicked'