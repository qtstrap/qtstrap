from qtstrap import *


class StateButton(QPushButton):
    state_changed = Signal(int)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if self._state != state:
            self._state = state
            self.state_changed.emit(self._state)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setIconSize(QSize(60, 60))
        self.icons = []
        self._state = None

        self.clicked.connect(self.next_state)
        self.state_changed.connect(self.update_icon)

    def next_state(self):
        self.state = (self.state + 1) % len(self.icons)

    def update_icon(self):
        if self.icons:
            self.setIcon(self.icons[self.state])


class IconToggleButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setIconSize(QSize(60, 60))
        self.setCheckable(True)

        self.icon_unchecked = QIcon()
        self.icon_checked = QIcon()

        self.clicked.connect(self.update_icon)

    def update_icon(self):
        if self.isChecked():
            self.setIcon(self.icon_checked)
        else:
            self.setIcon(self.icon_unchecked)


class ConfirmToggleButton(QPushButton):
    _state_changed = Signal(int)

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, state):
        if self._state != state:
            self._state = state
            self.timer.stop()
            self._state_changed.emit(self._state)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setIconSize(QSize(50, 50))
        self.icons = []

        self._state = None
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.uncheck)
        self.timeout_time = 1000

        self.clicked.connect(self.next_state)
        self._state_changed.connect(self.update_icon)

    def uncheck(self):
        self.state = 0
        self.setChecked(False)
        self.setCheckable(False)

    def confirm(self):
        self.state = 1
        self.timer.start(self.timeout_time)

    def check(self):
        self.state = 2
        self.setCheckable(True)
        self.setChecked(True)

    def next_state(self):
        if self.state == 0:
            self.confirm()
        elif self.state == 1:
            self.check()
        elif self.state == 2:
            self.uncheck()

    def update_icon(self):
        if self.icons:
            self.setIcon(self.icons[self.state])


class MenuButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._menu = QMenu(self)
        self.setMenu(self._menu)

    def addAction(self, *args, **kwargs):
        return self._menu.addAction(*args, **kwargs)


class ColorPickerButton(QToolButton):
    changed = Signal()

    def __init__(self, title: str, color: QColor | str, changed):
        super().__init__()
        self.title = title
        self.set_color(color)
        self.setToolTip(title)
        self.setMinimumSize(30, 30)

        self.clicked.connect(self.on_click)
        self.changed.connect(changed)

    def on_click(self):
        self.dialog = QColorDialog(self.color)
        self.dialog.setWindowTitle(self.title)
        self.dialog.setModal(True)
        self.dialog.show()
        self.dialog.colorSelected.connect(self.color_selected)

    def set_color(self, new_color: QColor | str):
        self.color = QColor(new_color)
        self.setStyleSheet(f'background:{self.color.name()}')

    def color_selected(self, new_color: QColor):
        self.set_color(new_color)
        self.changed.emit()
