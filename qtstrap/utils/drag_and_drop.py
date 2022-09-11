from __future__ import annotations
from qtstrap import *


def accepts_file_drops(extensions: str|[str]):
    """
    Decorator that enables drag-and-drop on a QWidget.
    Accepts a str or a list of strings of the valid file extensions.
    """

    # force extensions to a list of strings, even if provided a single string
    if isinstance(extensions, str):
        extensions = [extensions]

    # normalize leading periods
    extensions = [e.removeprefix('.') for e in extensions]

    # the method to add to the object
    def dragEnterEvent(self, event):
        prefix = 'file:///'
        strip = len(prefix)
        
        if event.mimeData().hasUrls():
            if len(event.mimeData().urls()) != 1:
                event.ignore()
                return
            text = event.mimeData().text()

            if not text.startswith('file:///'):
                event.ignore()
                return

            if text.split('.')[-1] not in extensions:
                event.ignore()
                return

            event.accept()
        else:
            event.ignore()

    def decorator(target):
        target.dragEnterEvent = dragEnterEvent
        return target

    return decorator
