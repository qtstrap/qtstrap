from qtstrap import *
from inspect import getmodule


class Inspector(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.obj_name = QLabel()
        self.obj_type = QLabel()
        self.base_type = QLabel()

        with CVBoxLayout(self, margins=2) as layout:
            layout.add(QLabel('Inspector'))
            with layout.hbox(margins=0):
                layout.add(QLabel('Name:'))
                layout.add(self.obj_name)
            with layout.hbox(margins=0):
                layout.add(QLabel('Type:'))
                layout.add(self.obj_type)
            with layout.hbox(margins=0):
                layout.add(QLabel('Base Type:'))
                layout.add(self.base_type)
            layout.add(QLabel(), 1)

    def inspect(self, item):
        for base in type(item.obj).__mro__:
            if 'QtWidgets' in getattr(getmodule(base), '__name__', ''):
                self.base_type.setText(base.__name__)
                break

        self.obj_name.setText(item.obj.objectName())
        self.obj_type.setText(type(item.obj).__name__)
