from qtstrap import *
import qtawesome as qta


class Panel(QWidget):
    """Base class for sidebar panels. Subclassing Panel is the registration.

    Subclasses define:
        name: unique identifier (used for lookup, required)
        display_name: human-readable name (shown in tooltip, optional — defaults to name)
        icon_name: qtawesome icon name (shown in activity bar, optional — defaults to a cog)

    Registration is automatic via __init_subclass__. No decorator, no manifest.
    """
    _registry: dict[str, type['Panel']] = {}

    name = ''
    display_name = ''
    icon_name = 'fa5s.cog'

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not getattr(cls, 'name', ''):
            raise TypeError(f'{cls.__name__} must define a name')
        if cls.name in Panel._registry:
            raise TypeError(f'{cls.__name__} duplicates panel name {cls.name!r}')
        Panel._registry[cls.name] = cls

    @property
    def display_name_resolved(self):
        return self.display_name or self.name


class Sidebar(QWidget):
    """Manages sidebar panels in a QStackedWidget.

    Reads from Panel._registry. Toggle via activity bar. Persists which
    panel is visible and whether sidebar is shown. Works on left or right
    side — the side only affects layout, not behavior.
    """

    def __init__(self, parent=None, side='left', name='sidebar'):
        super().__init__(parent=parent)
        self.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Expanding)
        self._side = side
        self._name = name
        self._panels: dict[str, Panel] = {}

        self.stack = QStackedWidget(self)

        with CHBoxLayout(self, margins=0) as layout:
            layout.add(self.stack)

        # Discover and instantiate all panel subclasses
        for panel_name, cls in Panel._registry.items():
            panel = cls(parent=self)
            self._panels[panel_name] = panel
            self.stack.addWidget(panel)

        # Initially hidden until a panel is selected
        self.hide()

    def register_panel(self, panel):
        """Explicitly register a panel instance (for dynamic/plugin loading)."""
        name = panel.name
        self._panels[name] = panel
        self.stack.addWidget(panel)

    def show_panel(self, name: str):
        """Show sidebar and switch to named panel."""
        if name in self._panels:
            self.show()
            self.stack.setCurrentWidget(self._panels[name])

    def toggle_panel(self, name: str) -> bool:
        """Toggle visibility of named panel. Returns True if now visible."""
        if name not in self._panels:
            return False

        current = self.stack.currentWidget()
        is_current = current and getattr(current, 'name', '') == name

        if self.isVisible() and is_current:
            self.hide()
            return False
        else:
            self.show_panel(name)
            return True

    def current_panel_name(self) -> str:
        """Return name of currently visible panel, or empty string if hidden."""
        if not self.isVisible():
            return ''
        widget = self.stack.currentWidget()
        return getattr(widget, 'name', '') if widget else ''

    def panels(self) -> dict[str, Panel]:
        return dict(self._panels)