from qtstrap import *
from qtstrap.extras.code_editor import CodeEditor


class CodeLine(CodeEditor):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setFixedHeight(28)

    def keyPressEvent(self, event:QKeyEvent):
        # emit ctrl+enter signal
        if event.modifiers() == Qt.ControlModifier:
            if event.key() in [Qt.Key_Enter, Qt.Key_Return]:
                self.ctrl_enter_pressed.emit()

        # definitely never print a newline
        if event.key() in [Qt.Key_Enter, Qt.Key_Return]:
            event.accept()
            return
        
        super().keyPressEvent(event)