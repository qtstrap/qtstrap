import qtpy
from qtpy import QtCore, QtGui, QtWidgets
from qtpy.QtCore import *
from qtpy.QtGui import *
from qtpy.QtWidgets import *


"""
helper that shortens signal connections

object.signal.connect(handler) -> object.signal(handler)

@object.signal
def handler():
    pass
"""
if qtpy.PYQT_VERSION:
    pyqtBoundSignal.__call__ = pyqtBoundSignal.connect
elif qtpy.PYSIDE_VERSION:
    SignalInstance.__call__ = SignalInstance.connect

"""
helper that allows for easily finding QObjects by name

some_widget['name_of_child']

@widget['button1'].clicked
def button1_hander():
    pass
"""
# QObject.__getitem__ = lambda self, name: self.findChild(QWidget, name)
