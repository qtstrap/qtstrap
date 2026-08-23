from qtstrap import *
from qtpy.QtCore import Qt


class StatusBarItem(QWidget):
    """Marker base class for auto-discovered status bar items.

    Subclass this and your widget appears in the status bar. The only
    requirement is being a QWidget subclass — the contribution IS the widget.
    """
    name = ''

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not getattr(cls, 'name', ''):
            raise TypeError(f'{cls.__name__} must define a name')
        if hasattr(StatusBarItem, '_registry'):
            if cls.name in StatusBarItem._registry:
                raise TypeError(f'{cls.__name__} duplicates status bar item name {cls.name!r}')
        else:
            StatusBarItem._registry = {}
        StatusBarItem._registry[cls.name] = cls

    _registry: dict[str, type['StatusBarItem']] = {}


class StatusBar(BaseToolbar):
    """Status bar with left and right zones.

    Left zone: status items (connection, sync, etc.)
    Right zone: actions and indicators (notifications, etc.)
    Separated by a stretchable spacer.

    Auto-discovers StatusBarItem subclasses for the left zone.
    Apps register custom items via add_item() or by subclassing StatusBarItem.
    """

    def __init__(self, parent, name='status_bar'):
        super().__init__(parent, name, location='bottom', size=30)

        self._left_items = []
        self._right_items = []

        # Auto-discover and instantiate status bar items
        for item_name, cls in StatusBarItem._registry.items():
            item = cls(self)
            self._left_items.append(item)
            self.addWidget(item)

        # Spacer between left and right zones
        self.add_spacer()

    def add_item(self, widget: QWidget, side='left'):
        """Add a widget to the status bar on the given side."""
        if side == 'left':
            # Insert before the spacer
            self._left_items.append(widget)
            self.insertWidget(len(self._left_items) - 1, widget)
        else:
            self._right_items.append(widget)
            self.addWidget(widget)

    def add_action(self, text: str, callback, side='right', shortcut=None):
        """Add an action button to the status bar."""
        btn = QToolButton(self)
        btn.setText(text)
        btn.clicked.connect(callback)
        self.add_item(btn, side=side)
        return btn