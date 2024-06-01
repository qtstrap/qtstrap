from qtpy.QtCore import Qt
from qtpy.QtWidgets import QDockWidget, QWidget


class BaseDockWidget(QDockWidget):
    _title = ''
    _starting_area = Qt.BottomDockWidgetArea
    _shortcut = ''
    _features = QDockWidget.DockWidgetClosable | QDockWidget.DockWidgetMovable | QDockWidget.DockWidgetFloatable

    def __init__(self, parent=None):
        super().__init__(self._title, parent=parent)
        self.setObjectName(self._title.replace(' ', ''))

        self._widget = QWidget()
        self.setWidget(self._widget)

        self.setFeatures(self._features)

        if not parent.restoreDockWidget(self):
            parent.addDockWidget(self._starting_area, self)
            self.hide()

        self.closeEvent = lambda x: self.hide()

    def toggleViewAction(self):
        action = super().toggleViewAction()
        if self._shortcut:
            action.setShortcut(self._shortcut)
        return action
