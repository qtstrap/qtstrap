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
helper that allows async functions to be connected to signals directly

button.clicked.connect(sync_handler)   # works as before
button.clicked.connect(async_handler)  # auto-wraps with promisify

sync functions pass through with zero overhead; async functions get
eagerly scheduled as asyncio tasks via promisify.
"""
if qtpy.PYSIDE_VERSION:
    _orig_connect = SignalInstance.connect

    def _smart_connect(self, slot, *args, **kwargs):
        import asyncio
        import inspect
        if inspect.iscoroutinefunction(slot):
            from qtstrap.extras.promise import promisify
            slot = promisify(slot)
        return _orig_connect(self, slot, *args, **kwargs)

    SignalInstance.connect = _smart_connect

"""
helper that allows for easily finding QObjects by name

some_widget['name_of_child']

@widget['button1'].clicked
def button1_hander():
    pass
"""
# QObject.__getitem__ = lambda self, name: self.findChild(QWidget, name)
