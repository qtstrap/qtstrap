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


def draggable(target):
    old_init = target.__init__

    def new_init(self, *args, **kwargs):
        old_init(self, *args, **kwargs)
        
        self.drag_start_position = None

    def new_mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def new_mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() != Qt.LeftButton:
            return

        if self.drag_start_position is None:
            return

        distance_moved = QPoint(event.pos() - self.drag_start_position).manhattanLength()
        if distance_moved < QApplication.startDragDistance():
            return
        
        if hasattr(self, 'get_drag_data'):
            mime = self.get_drag_data()
        else:
            mime = QMimeData()
            mime.setText('test_drop_please_ignore')

        drop = PreviewDrag(self, mimedata=mime).exec_()

        if hasattr(self, 'handle_drop'):
            self.handle_drop(drop)

        self.drag_start_position = None
    
    target.__init__ = new_init
    target.mousePressEvent = new_mousePressEvent
    target.mouseMoveEvent = new_mouseMoveEvent

    return target


class PreviewDrag(QDrag):
    def __init__(self, source, mimedata=None):
        super().__init__(source)

        pixmap = QPixmap(source.size())
        source.render(pixmap)
        self.setPixmap(pixmap)

        if mimedata:
            self.setMimeData(mimedata)