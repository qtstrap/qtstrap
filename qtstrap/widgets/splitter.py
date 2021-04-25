from qtstrap import *
from .layouts import *


class CSplitter(QSplitter):
    def __init__(self, parent=None, orientation=None, **kwargs):
        if isinstance(parent, QWidget):
            super().__init__(parent, **kwargs)
            CHBoxLayout(parent).add(self)
        elif isinstance(parent, QLayout):
            super().__init__(**kwargs)
            parent.add(self)
        
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