from qtstrap import *


class LabelEdit(QWidget):
    text_changed = Signal(str)

    def __init__(self, text, *args, changed=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.setToolTip('doubleclick to edit')

        self.label = QLabel(text)
        self.edit = QLineEdit()
        self.edit.installEventFilter(self)

        self.stack = QStackedLayout(self)
        self.stack.insertWidget(0, self.label)
        self.stack.insertWidget(1, self.edit)

        if changed:
            self.text_changed.connect(changed)

    def text(self):
        return self.label.text()

    def setText(self, text):
        self.label.setText(text)
        self.text_changed.emit(self.edit.text())

    def start_editing(self):
        self.edit.setText(self.label.text())
        self.edit.setFocus()
        self.stack.setCurrentIndex(1)

    def mouseDoubleClickEvent(self, event: QtGui.QMouseEvent) -> None:
        self.start_editing()
        return super().mouseDoubleClickEvent(event)

    def accept(self):
        self.setText(self.edit.text())
        self.stack.setCurrentIndex(0)

    def dismiss(self):
        self.stack.setCurrentIndex(0)

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                self.accept()
                return True
            
            if event.key() == QtCore.Qt.Key_Escape:
                self.dismiss()
                event.accept()
                return True

        return False