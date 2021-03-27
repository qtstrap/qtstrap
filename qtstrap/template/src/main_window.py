from qtstrap import *


"""
main_window.py



"""


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        with CVBoxLayout(self) as layout:
            layout.add(QLabel("Hello world!"))