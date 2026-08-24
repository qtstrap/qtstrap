from qtstrap import *
from qtpy.QtCore import Qt


class StatusBarItem(QWidget):
    """Marker base class for auto-discovered status bar items.

    Subclass this and your widget appears in the status bar. The only
    requirement is being a QWidget subclass — the contribution IS the widget.

    Class attributes:
        name: unique identifier (used for lookup via get_item)
        side: 'left' or 'right' — which zone to place the item in
    """
    name = ''
    side = 'left'

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

        # Inner containers for left/right zones — avoids index math on QToolBar
        self._left_container = QWidget(self)
        self._left_layout = QHBoxLayout(self._left_container)
        self._left_layout.setContentsMargins(0, 0, 0, 0)
        self._left_layout.setSpacing(4)

        self._right_container = QWidget(self)
        self._right_layout = QHBoxLayout(self._right_container)
        self._right_layout.setContentsMargins(0, 0, 0, 0)
        self._right_layout.setSpacing(4)

        # Spacer between left and right zones
        self._spacer = QWidget(self)
        self._spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        # Add containers to toolbar: left | spacer | right
        self.addWidget(self._left_container)
        self.addWidget(self._spacer)
        self.addWidget(self._right_container)

        # Auto-discover and instantiate status bar items.
        # If the class was wrapped with @singleton, use the wrapper so the
        # subsystem that owns the singleton gets the same instance displayed.
        self._items = {}
        for item_name, cls in StatusBarItem._registry.items():
            factory = getattr(cls, '_singleton_wrapper', cls)
            item = factory(self)
            self._items[cls.name] = item
            side = getattr(cls, 'side', 'left')
            if side == 'right':
                self._right_layout.addWidget(item)
            else:
                self._left_layout.addWidget(item)

    def get_item(self, name: str) -> QWidget:
        """Recover a reference to an auto-discovered status bar item by name."""
        return self._items.get(name)

    def add_item(self, widget: QWidget, side='left'):
        """Add a widget to the status bar on the given side."""
        if side == 'left':
            self._left_layout.addWidget(widget)
        else:
            self._right_layout.addWidget(widget)

    def add_action(self, text: str, callback, side='right', shortcut=None):
        """Add an action button to the status bar."""
        btn = QToolButton(self)
        btn.setText(text)
        btn.clicked.connect(callback)
        self.add_item(btn, side=side)
        return btn