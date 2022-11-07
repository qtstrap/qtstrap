from qtstrap import *
import qtawesome as qta


location_map = {
    'left': Qt.LeftToolBarArea,
    'right': Qt.RightToolBarArea,
    'top': Qt.TopToolBarArea,
    'bottom': Qt.BottomToolBarArea,
}


class BaseToolbar(QToolBar):
    def __init__(self, parent=None, name=None, location=None, size=40, **kwargs):
        super().__init__(parent=parent, **kwargs)

        self.setMovable(False)
        self.setContextMenuPolicy(Qt.PreventContextMenu)
        self.setIconSize(QSize(size, size))
        if name:
            self.setObjectName(name)
        if location and parent:
            if isinstance(location, str):
                location = location_map[location]
            parent.addToolBar(location, self)

    def add_spacer(self):
        empty = QWidget(self)
        empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addWidget(empty)
