from qtstrap import *


class Repl(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        with CVBoxLayout(self, margins=2) as layout:
            layout.add(QLabel('REPL'))


class ReplDockWidget(BaseDockWidget):
    _title = 'REPL'
    _starting_area = Qt.BottomDockWidgetArea
    _shortcut = 'Ctrl+R'

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.repl = Repl(self)
        self.setWidget(self.repl)
