from qtstrap import *


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.button = QPushButton('Click me!', clicked=lambda: self.label.setText('clicked'))
        self.label = QLabel('^^^^^^^')

        with CVBoxLayout(self) as layout:
            layout.add(self.button)
            layout.add(self.label)


def test_base_window_startup(qtbot):
    window = MainWindow()

    qtbot.addWidget(window)
    assert window.label.text() == '^^^^^^^'

    qtbot.mouseClick(window.button, QtCore.Qt.LeftButton)
    assert window.label.text() == 'clicked'


# def test_base_window_settings(qtbot):
#     window = MainWindow()

#     qtbot.addWidget(window)
#     assert window.geometry() == QRect(0, 0, 640, 480)

#     window.setGeometry(100, 100, 640, 480)
#     assert window.geometry() == QRect(100, 100, 640, 480)

#     window.close()
    
#     window = MainWindow()
    
#     qtbot.addWidget(window)
#     assert window.geometry() == QRect(100, 100, 640, 480)