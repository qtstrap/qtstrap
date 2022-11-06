from qtstrap import *
import qtawesome as qta


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
        empty.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.addWidget(empty)


class SettingsToolbar(BaseToolbar):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.settings_button = QToolButton(self, icon=qta.icon('fa.gear', color='gray'))
        self.addWidget(self.settings_button)

        self.settings_menu = QMenu(self.settings_button)
        self.settings_button.setMenu(self.settings_menu)
        self.settings_button.setPopupMode(QToolButton.InstantPopup)

        self.add_action('&Exit', shortcut='Ctrl+Q', statusTip='Exit application').triggered.connect(App.close)

    def add_action(self, *args, **kwargs):
        return self.settings_menu.addAction(*args, **kwargs)

    def add_separator(self):
        self.settings_menu.addSeparator()
