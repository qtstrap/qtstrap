from qtstrap import *
import qtawesome as qta
from .panel import Panel, Sidebar


class ActivityBar(BaseToolbar):
    """Icon strip that toggles sidebar panels.

    Auto-populates from a Sidebar's registered panels. A settings button
    is included by default at the bottom.

    Works with any object exposing `toggle_panel(name) -> bool` and
    `panels() -> dict` — duck typing, not isinstance(Sidebar).
    """

    def __init__(self, parent, sidebar, name='activity_bar'):
        super().__init__(parent, name, location='left', size=40)
        self._sidebar = sidebar

        self._buttons: dict[str, QToolButton] = {}

        # Create a button for each panel
        panels = sidebar.panels() if hasattr(sidebar, 'panels') else {}
        for panel_name, panel in panels.items():
            icon_name = getattr(panel, 'icon_name', 'fa5s.cog')
            display_name = getattr(panel, 'display_name_resolved', panel_name) \
                if hasattr(panel, 'display_name_resolved') \
                else getattr(panel, 'display_name', panel_name) or panel_name

            btn = QToolButton(self)
            btn.setIcon(qta.icon(icon_name))
            btn.setToolTip(display_name)
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, n=panel_name: self._on_click(n))
            self.addWidget(btn)
            self._buttons[panel_name] = btn

        self.add_spacer()

        # Settings button (bottom)
        self.settings_btn = QToolButton(self)
        self.settings_btn.setIcon(qta.icon('fa5s.cog'))
        self.settings_btn.setToolTip('Settings')
        self.settings_btn.setPopupMode(QToolButton.InstantPopup)
        self.settings_menu = QMenu()
        self.settings_btn.setMenu(self.settings_menu)
        self.addWidget(self.settings_btn)

    def _on_click(self, panel_name: str):
        visible = self._sidebar.toggle_panel(panel_name)
        self._buttons[panel_name].setChecked(visible)

    @property
    def settings_menu(self):
        return self._settings_menu

    @settings_menu.setter
    def settings_menu(self, menu):
        self._settings_menu = menu

    def add_settings_action(self, text: str, callback, shortcut=None):
        """Add an action to the settings menu."""
        action = self._settings_menu.addAction(text)
        action.triggered.connect(callback)
        if shortcut:
            action.setShortcut(shortcut)
        return action