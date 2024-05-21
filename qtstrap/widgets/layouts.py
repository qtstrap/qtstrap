from typing import TypeAlias, Literal, Sequence
from qtpy.QtCore import (
    Qt,
    QSettings,
    QMargins,
)
from qtpy.QtWidgets import (
    QMainWindow,
    QWidget,
    QLayout,
    QSplitter,
    QVBoxLayout,
    QHBoxLayout,
    QGridLayout,
    QFormLayout,
    QScrollArea,
)


alignments = {
    'left': Qt.AlignLeft,
    'l': Qt.AlignLeft,
    'right': Qt.AlignRight,
    'r': Qt.AlignRight,
    'top': Qt.AlignTop,
    't': Qt.AlignTop,
    'bottom': Qt.AlignBottom,
    'bot': Qt.AlignBottom,
    'b': Qt.AlignBottom,
    'center': Qt.AlignCenter,
    'c': Qt.AlignCenter,
}

AlignmentType: TypeAlias = (
    Literal[
        Qt.AlignLeft,
        Qt.AlignRight,
        Qt.AlignTop,
        Qt.AlignBottom,
        Qt.AlignCenter,
        'left',
        'l',
        'right',
        'r',
        'top',
        't',
        'bottom',
        'bot',
        'b',
        'center',
        'c',
    ]
    | None
)

orientations = {
    'horizontal': Qt.Horizontal,
    'h': Qt.Horizontal,
    'vertical': Qt.Vertical,
    'v': Qt.Vertical,
}

OrientationType: TypeAlias = (
    Literal[
        Qt.Horizontal,
        Qt.Horizontal,
        Qt.Vertical,
        Qt.Vertical,
        'horizontal',
        'h',
        'vertical',
        'v',
    ]
    | None
)

MarginsType: TypeAlias = QMargins | tuple | int | None


class ContextLayoutBase:
    def add(
        self, item: QWidget | QLayout | Sequence[QWidget | QLayout], *args, **kwargs
    ) -> QWidget | QLayout | Sequence[QWidget | QLayout]:
        return item

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class ContextLayout(ContextLayoutBase):
    def __init__(
        self,
        parent: QMainWindow | QSplitter | QWidget | ContextLayoutBase | None = None,
        stretch: int | None = None,
        margins: QMargins | tuple | int | None = None,
        align: AlignmentType = None,
        **kwargs,
    ):
        if isinstance(parent, QMainWindow):
            # a layout can't be added directly to a QMainWindow, because it requires a "centralWidget"
            # we can use a throwaway QWidget as a shim
            widget = QWidget(parent=parent)
            parent.setCentralWidget(widget)
            super().__init__(widget, **kwargs)
        elif isinstance(parent, QSplitter):
            # a layout can't be added directly to a QSplitter, only a widget
            # we can use a throwaway QWidget as a shim
            widget = QWidget(parent=parent)
            parent.addWidget(widget)
            super().__init__(widget, **kwargs)
        elif parent is None or isinstance(parent, QWidget):
            super().__init__(parent, **kwargs)
        else:
            super().__init__(**kwargs)
            if stretch:
                parent.addLayout(self, stretch)
            else:
                parent.addLayout(self)

        if margins is not None:
            if isinstance(margins, tuple):
                self.setContentsMargins(*margins)
            elif isinstance(margins, int):
                self.setContentsMargins(margins, margins, margins, margins)

        if align in alignments:
            self.setAlignment(alignments[align])

        self._stack: list[ContextLayoutBase] = []
        self.next_layout: ContextLayoutBase | None = None

    def __getattr__(self, name: str):
        return getattr(self._layout, name)

    @property
    def _layout(self):
        layout = self
        if len(self._stack) > 0:
            layout = self._stack[len(self._stack) - 1]
        return layout

    def __call__(self):
        return self._layout

    def __add__(
        self,
        item: QWidget | QLayout | Sequence[QWidget | QLayout],
    ) -> QWidget | QLayout | Sequence[QWidget | QLayout]:
        self.add(item)
        return item

    def __iadd__(
        self,
        item: QWidget | QLayout | Sequence[QWidget | QLayout],
    ):
        self.add(item)
        return self

    def add(
        self,
        item: QWidget | QLayout | Sequence[QWidget | QLayout],
        *args,
        **kwargs,
    ) -> QWidget | QLayout | Sequence[QWidget | QLayout]:
        if isinstance(item, QWidget):
            self._layout.addWidget(item, *args, **kwargs)
        elif isinstance(item, QLayout):
            self._layout.addLayout(item, *args, **kwargs)
        elif isinstance(item, Sequence):
            for i in item:
                self._layout.add(i, *args, **kwargs)

        return item

    def vbox(self, *args, **kwargs):
        self.next_layout = CVBoxLayout(self._layout, *args, **kwargs)
        return self

    def hbox(self, *args, **kwargs):
        self.next_layout = CHBoxLayout(self._layout, *args, **kwargs)
        return self

    def grid(self, *args, **kwargs):
        self.next_layout = CGridLayout(self._layout, *args, **kwargs)
        return self

    def form(self, *args, **kwargs):
        self.next_layout = CFormLayout(self._layout, *args, **kwargs)
        return self

    def split(self, name: str | None = None, **kwargs):
        if name:
            self.next_layout = PersistentCSplitter(name, self._layout, **kwargs)
        else:
            self.next_layout = CSplitter(self._layout, **kwargs)
        return self

    def scroll(self, name: str | None = None, **kwargs):
        if name:
            self.next_layout = PersistentCScrollArea(name, self._layout, **kwargs)
        else:
            self.next_layout = CScrollArea(self._layout, **kwargs)
        return self

    def __enter__(self):
        if self.next_layout is not None:
            self.next_layout.__enter__()
            self._stack.append(self.next_layout)
            self.next_layout = None
        return self

    def __exit__(self, *_):
        if len(self._stack) > 0:
            item = self._stack.pop()
            item.__exit__()


# *************************************************************************** #


class CVBoxLayout(ContextLayout, QVBoxLayout): ...


class CHBoxLayout(ContextLayout, QHBoxLayout): ...


class CGridLayout(ContextLayout, QGridLayout):
    ...

    def addWidget(
        self,
        item: QWidget,
        row: int,
        column: int,
        row_span: int = 1,  # positional only
        column_span: int = 1,  # positional only
        *,
        rowSpan: int = 1,  # named only
        columnSpan: int = 1,  # named only
        **kwargs,
    ) -> None:
        """Change the function signature to allow using the spans as named params"""
        rspan = rowSpan if rowSpan != 1 else row_span
        cspan = columnSpan if columnSpan != 1 else column_span
        super().addWidget(item, row, column, rspan, cspan, **kwargs)

    def addLayout(
        self,
        item: QLayout,
        row: int,
        column: int,
        row_span: int = 1,  # positional only
        column_span: int = 1,  # positional only
        *,
        rowSpan: int = 1,  # named only
        columnSpan: int = 1,  # named only
        **kwargs,
    ) -> None:
        """Change the function signature to allow using the spans as named params"""
        rspan = rowSpan if rowSpan != 1 else row_span
        cspan = columnSpan if columnSpan != 1 else column_span
        super().addLayout(item, row, column, rspan, cspan, **kwargs)


class CFormLayout(ContextLayout, QFormLayout):
    def __add__(
        self,
        item: tuple[str, QWidget | QLayout],
    ) -> QWidget | QLayout:
        self.add(item)
        return item[1]

    def __iadd__(
        self,
        item: tuple[str, QWidget | QLayout],
    ):
        self.add(item)
        return self

    def add(
        self,
        a: str
        | QWidget
        | QLayout
        | tuple[str, QWidget | QLayout]
        | Sequence[tuple[str, QWidget | QLayout]]
        | dict[str, QWidget | QLayout],
        b: QWidget = None,
    ):
        if b is not None:
            self._layout.addRow(a, b)
            return b

        if isinstance(a, Sequence):
            if isinstance(a[0], (str, QWidget, QLayout)):
                self._layout.addRow(*a)
                return a[1]
            if isinstance(a[0], Sequence):
                for item in a:
                    self._layout.addRow(*item)
                return a
        if isinstance(a, dict):
            for name, obj in a.items():
                self._layout.addRow(name, obj)

        return b


# --------------------------------------------------------------------------- #


class CSplitter(QSplitter, ContextLayoutBase):
    def __init__(
        self,
        parent: QWidget | QLayout | ContextLayoutBase | None = None,
        margins: QMargins | tuple | int | None = None,
        orientation: OrientationType | None = None,
        **kwargs,
    ):
        if orientation in orientations:
            orientation = orientations[orientation]

        if isinstance(parent, QWidget):
            super().__init__(parent, orientation, **kwargs)
            CHBoxLayout(parent, margins=margins).add(self)
        elif isinstance(parent, ContextLayoutBase):
            super().__init__(orientation, **kwargs)
            parent.add(self)
        elif isinstance(parent, QLayout):
            # TODO: implement this
            pass

        if margins is not None:
            if isinstance(margins, tuple):
                self.setContentsMargins(*margins)
            elif isinstance(margins, int):
                self.setContentsMargins(margins, margins, margins, margins)

        if orientation:
            self.setOrientation(orientation)

    def __iadd__(
        self,
        item: QWidget | QLayout | Sequence[QWidget | QLayout],
    ):
        self.add(item)
        return self

    def add(
        self,
        item: QWidget | QLayout | Sequence[QWidget | QLayout],
        stretch: int | None = None,
    ) -> QWidget | QLayout | Sequence[QWidget | QLayout]:
        if isinstance(item, QWidget):
            self.addWidget(item)
            if stretch:
                self.setStretchFactor(self.count() - 1, stretch)
        elif isinstance(item, QLayout):
            self.addWidget(QWidget(self, layout=item))
            if stretch:
                self.setStretchFactor(self.count() - 1, stretch)
        elif isinstance(item, Sequence):
            for i in item:
                self.add(i)
        return item

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class PersistentCSplitter(CSplitter, ContextLayoutBase):
    def __init__(
        self,
        name: str,
        parent: QWidget | QLayout | ContextLayoutBase | None = None,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        self.name: str = name

        self.splitterMoved.connect(lambda: QSettings().setValue(self.name, self.saveState()))

    def restore_state(self):
        if state := QSettings().value(self.name, None):
            self.restoreState(state)

    def __exit__(self, *args):
        self.restore_state()


# --------------------------------------------------------------------------- #


class CScrollArea(QScrollArea, ContextLayoutBase):
    def __init__(
        self,
        parent: QWidget | QLayout | ContextLayoutBase | None = None,
        margins: QMargins | tuple | int | None = None,
        orientation: OrientationType = None,
        **kwargs,
    ):
        super().__init__(**kwargs)

        if isinstance(parent, QWidget):
            CVBoxLayout(parent).add(self)
        elif isinstance(parent, ContextLayoutBase):
            parent.add(self)
        elif isinstance(parent, QLayout):
            parent.addLayout(self)

        widget = QWidget()
        layout = CVBoxLayout(widget)
        layout.setAlignment(Qt.AlignTop)
        self.setWidget(widget)
        self.setWidgetResizable(True)

        if margins:
            self.setContentsMargins(*margins)

        if orientation:
            if orientation in orientations:
                orientation = orientations[orientation]
            self.setOrientation(orientation)

    def __iadd__(
        self,
        item: QWidget | QLayout | Sequence[QWidget | QLayout],
    ):
        self.add(item)
        return self

    def add(
        self,
        item: QWidget | QLayout | Sequence[QWidget | QLayout],
        stretch: int = None,
    ) -> QWidget | QLayout | Sequence[QWidget | QLayout]:
        if isinstance(item, QWidget):
            self.widget().layout().addWidget(item)
            if stretch:
                self.widget().layout().setStretchFactor(self.count() - 1, stretch)
        elif isinstance(item, QLayout):
            self.addWidget(QWidget(self, layout=item))
            if stretch:
                self.setStretchFactor(self.count() - 1, stretch)
        elif isinstance(item, Sequence):
            for i in item:
                self.add(i)
        return item

    def addWidget(self, *args, **kwargs):
        self.widget().layout().addWidget(*args, **kwargs)

    def addLayout(self, *args, **kwargs):
        self.widget().layout().addLayout(*args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class PersistentCScrollArea(QScrollArea, ContextLayoutBase):
    def __init__(
        self,
        name: str,
        parent: QWidget | QLayout | ContextLayoutBase | None = None,
        **kwargs,
    ):
        super().__init__(parent, **kwargs)
        self.name = name

        self.scrolled.connect(lambda: QSettings().setValue(self.name, self.saveState()))

    def scroll_to(self, value: int):
        self.verticalScrollBar().setValue(value)

    def restore_state(self):
        if state := QSettings().value(self.name, None):
            self.restoreState(state)

    def __exit__(self, *args):
        self.restore_state()
