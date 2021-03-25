from .qt import *


location_map = {
    'left': Qt.LeftToolBarArea,
    'right': Qt.RightToolBarArea,
    'top': Qt.TopToolBarArea,
    'bottom': Qt.BottomToolBarArea,
}


class BaseToolbar(QToolBar):
    def __init__(self, parent=None, name=None, location=None, size=40):
        super().__init__(parent=parent)

        self.setMovable(False)
        self.setIconSize(QSize(size, size))
        if name:
            self.setObjectName(name)
        if location and parent:
            if isinstance(location, str):
                location = location_map[location]
            parent.addToolBar(location, self)

    def add_spacer(self):
        empty = QWidget(self)
        empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding);
        self.addWidget(empty)