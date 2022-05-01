from qtstrap import *
from .editor import CodeEditor


class CodeLine(CodeEditor):
    def __init__(self, *args, changed, words, **kwargs):
        super().__init__(*args, **kwargs)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setLineWrapMode(QTextEdit.NoWrap)
        self.setFixedHeight(28)
        self.textChanged.connect(changed)

        self.completer = QCompleter(words, self)
        self.completer.setModelSorting(QCompleter.CaseInsensitivelySortedModel)
        self.completer.setWidget(self)
        self.completer.popup().setMinimumWidth(150)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setFilterMode(Qt.MatchContains)

        self.completer.activated.connect(self.insert_completion)

    def insert_completion(self, completion):
        tc = self.textCursor()
        extra = len(completion) - len(self.completer.completionPrefix())
        tc.movePosition(QTextCursor.Left)
        tc.movePosition(QTextCursor.EndOfWord)
        tc.insertText(completion[-extra:])
        self.setTextCursor(tc)

    def text_under_cursor(self):
        tc = self.textCursor()
        tc.select(QTextCursor.WordUnderCursor)
        return tc.selectedText()

    def keyPressEvent(self, event: PySide2.QtCore.QEvent):
        force_popup = False
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_Space:
                force_popup = True

        keys = [Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab]
        if self.completer.popup().isVisible():
            if event.key() in keys:
                event.ignore()
                return
    
        if event.key() in [Qt.Key_Enter, Qt.Key_Return]:
            event.accept()
            return

        braces = {
            '"': '"',
            "'": "'",
            '{': '}',
            '(': ')',
            '<': '>',
            '[': ']',
            '|': '|',
            '`': '`',
        }

        cur = self.textCursor()
        if cur.hasSelection():
            if event.text() in braces:
                start = cur.selectionStart()
                end = cur.selectionEnd()
                cur.clearSelection()
                cur.setPosition(end)
                cur.insertText(braces[event.text()])
                cur.setPosition(start)
                cur.insertText(event.text())
                cur.movePosition(QTextCursor.WordRight, QTextCursor.KeepAnchor)
                self.setTextCursor(cur)
                return

        super().keyPressEvent(event)

        prefix = self.text_under_cursor()
        if prefix or force_popup:
            self.completer.setCompletionPrefix(prefix)
            index = self.completer.completionModel().index(0, 0)
            self.completer.popup().setCurrentIndex(index)

            cr = self.cursorRect()
            cr.setWidth(self.completer.popup().sizeHintForColumn(0) + self.completer.popup().verticalScrollBar().sizeHint().width())
            self.completer.complete(cr)
        else:
            self.completer.popup().hide()

    def text(self):
        return self.toPlainText()