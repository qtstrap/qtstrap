from qtstrap import *
# from .splitter import CSplitter, PersistentCSplitter


alignments = {
    'left': Qt.AlignLeft,
    'right': Qt.AlignRight,
    'top': Qt.AlignTop,
    'bot': Qt.AlignBottom,
    'bottom': Qt.AlignBottom,
    'center': Qt.AlignCenter,
}


orientations = {
    'h': Qt.Horizontal,
    'horizontal': Qt.Horizontal,
    'v': Qt.Vertical,
    'vertical': Qt.Vertical,
}


class ContextLayout:
    def __init__(self, parent=None, stretch=None, margins=None, align=None, **kwargs):
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

        if margins:
            self.setContentsMargins(*margins)

        if align in alignments:
            self.setAlignment(alignments[align])

        self._stack = []
        self.next_layout = None

    def __getattr__(self, name):
        return getattr(self._layout, name)

    @property
    def _layout(self):
        layout = self
        if len(self._stack) > 0:
            layout = self._stack[len(self._stack) - 1]
        return layout

    def __call__(self):
        return self._layout

    def add(self, item, *args, **kwargs):
        if isinstance(item, QWidget):
            self._layout.addWidget(item, *args, **kwargs)
        elif isinstance(item, QLayout):
            self._layout.addLayout(item, *args, **kwargs)
        elif isinstance(item, list):
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

    def split(self, name=None, **kwargs):
        if name:
            self.next_layout = PersistentCSplitter(name, self._layout, **kwargs)
        else:
            self.next_layout = CSplitter(self._layout, **kwargs)
        return self

    def scroll(self, name=None, **kwargs):
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


class CVBoxLayout(ContextLayout, QVBoxLayout):
    pass


class CHBoxLayout(ContextLayout, QHBoxLayout):
    pass


class CGridLayout(ContextLayout, QGridLayout):
    pass


# --------------------------------------------------------------------------- #


class CSplitter(QSplitter):
    def __init__(self, parent=None, margins=None, orientation=None, **kwargs):
        if orientation in orientations:
            orientation = orientations[orientation]

        if isinstance(parent, QWidget):
            super().__init__(parent, orientation, **kwargs)
            CHBoxLayout(parent).add(self)
        elif isinstance(parent, QLayout):
            super().__init__(orientation, **kwargs)
            parent.add(self)

        if margins:
            self.setContentsMargins(*margins)

        if orientation:
            self.setOrientation(orientation)

    def add(self, item, stretch=None):
        if isinstance(item, QWidget):
            self.addWidget(item)
            if stretch:
                self.setStretchFactor(self.count()-1, stretch)
        elif isinstance(item, QLayout):
            self.addWidget(QWidget(self, layout=item))
            if stretch:
                self.setStretchFactor(self.count()-1, stretch)
        elif isinstance(item, list):
            for i in item:
                self.add(i)
        return item

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class PersistentCSplitter(CSplitter):
    def __init__(self, name, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.name = name

        self.splitterMoved.connect(lambda: QSettings().setValue(self.name, self.saveState()))
    
    def restore_state(self):
        if state := QSettings().value(self.name, None):
            self.restoreState(state)

    def __exit__(self, *args):
        self.restore_state()


# --------------------------------------------------------------------------- #


class CScrollArea(QScrollArea):
    def __init__(self, parent=None, margins=None, orientation=None, **kwargs):
        super().__init__(**kwargs)

        if isinstance(parent, QWidget):
            CVBoxLayout(parent).add(self)
        elif isinstance(parent, QLayout):
            parent.add(self)

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

    def add(self, item, stretch=None):
        if isinstance(item, QWidget):
            self.widget().layout().addWidget(item)
            if stretch:
                self.widget().layout().setStretchFactor(self.count()-1, stretch)
        elif isinstance(item, QLayout):
            self.addWidget(QWidget(self, layout=item))
            if stretch:
                self.setStretchFactor(self.count()-1, stretch)
        elif isinstance(item, list):
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


class PersistentCScrollArea(QScrollArea):
    def __init__(self, name, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.name = name

        self.scrolled.connect(lambda: QSettings().setValue(self.name, self.saveState()))
    
        
    def scroll_to(self, value):
        self.verticalScrollBar().setValue(value)

    def restore_state(self):
        if state := QSettings().value(self.name, None):
            self.restoreState(state)

    def __exit__(self, *args):
        self.restore_state()
