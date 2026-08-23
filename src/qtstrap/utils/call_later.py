from qtpy.QtCore import QTimer, QCoreApplication


def call_later(what, msec: int = 1):
    """call the given function after a specified delay"""
    parent = QCoreApplication.instance()
    timer = QTimer(parent, singleShot=True)
    timer.timeout.connect(what)
    timer.timeout.connect(timer.deleteLater)
    timer.start(msec)
