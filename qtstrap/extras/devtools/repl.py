from qtstrap import *


class ReplDockWidget(BaseDockWidget):
    _title = 'REPL'
    _starting_area = Qt.BottomDockWidgetArea
    _shortcut = 'Ctrl+R'

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        with CVBoxLayout(self._widget, margins=2) as layout:
            layout.add(QLabel('REPL goes here'))