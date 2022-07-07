from qtstrap import *


class CodeEditor(QTextEdit):
    def __init__(self, *args, changed=None, model=None, highlighter=None, **kwargs):
        super().__init__(*args, **kwargs)

        set_font_options(self, {
            'setFamily': 'Courier',
            'setStyleHint': QFont.Monospace,
            'setFixedPitch': True,
        })
        
        self.installEventFilter(self)
        self.update_tab_width()

        if highlighter:
            self.syntax = highlighter(self)
        
        if changed:
            self.textChanged.connect(changed)

        self.model = model

        self.completer = QCompleter(self.model, self)
        self.completer.setWidget(self)
        self.completer.popup().setMinimumWidth(150)
        self.completer.setCompletionMode(QCompleter.UnfilteredPopupCompletion)

        self.completer.activated.connect(self.insert_completion)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.FontChange:
            self.update_tab_width()
            return False

        return False

    def update_tab_width(self):
        if qtpy.QT5:
            self.setTabStopWidth(QFontMetricsF(self.font()).width(' ') * 4)
        elif qtpy.QT6:
            self.setTabStopWidth(QFontMetricsF(self.font()).maxWidth() * 4)

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
        
    def keyPressEvent(self, event:QKeyEvent):
        force_popup = False
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_Space:
                force_popup = True

        keys = [Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab]
        if self.completer.popup().isVisible():
            if event.key() in keys:
                event.ignore()
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

        if event.modifiers() == Qt.AltModifier:
            if event.key() == Qt.Key_Up:
                cur.beginEditBlock()

                og_start = cur.selectionStart()
                og_end = cur.selectionEnd()
                cur.setPosition(og_start)
                cur.movePosition(QTextCursor.StartOfLine)
                start = cur.selectionStart()
                cur.setPosition(og_end)
                cur.movePosition(QTextCursor.EndOfLine)
                end = cur.selectionEnd()

                cur.setPosition(start)
                cur.setPosition(end + 1, QTextCursor.KeepAnchor)
                
                self.setTextCursor(cur)

                text = cur.selectedText()
                cur.removeSelectedText()

                cur.movePosition(QTextCursor.Up)
                cur.movePosition(QTextCursor.StartOfLine)

                self.setTextCursor(cur)

                cur.insertText(text)
                cur.movePosition(QTextCursor.Up)
                self.setTextCursor(cur)

                cur.endEditBlock()
                event.ignore()
                return

            if event.key() == Qt.Key_Down:
                cur.beginEditBlock()
                og_start = cur.selectionStart()
                og_end = cur.selectionEnd()
                cur.setPosition(og_start)
                cur.movePosition(QTextCursor.StartOfLine)
                start = cur.selectionStart()
                cur.setPosition(og_end)
                cur.movePosition(QTextCursor.EndOfLine)
                end = cur.selectionEnd()

                cur.setPosition(start)
                cur.setPosition(end + 1, QTextCursor.KeepAnchor)
                
                self.setTextCursor(cur)

                text = cur.selectedText()
                cur.removeSelectedText()

                cur.movePosition(QTextCursor.Down)
                cur.movePosition(QTextCursor.StartOfLine)

                self.setTextCursor(cur)

                cur.insertText(text)
                cur.movePosition(QTextCursor.Up)
                self.setTextCursor(cur)

                cur.endEditBlock()
                event.ignore()
                return

        if cur.hasSelection():
            if event.key() in [Qt.Key_Tab, Qt.Key_Backtab]:
                cur.beginEditBlock()

                og_start = cur.selectionStart()
                og_end = cur.selectionEnd()
                cur.setPosition(og_start)
                cur.movePosition(QTextCursor.StartOfLine)
                start = cur.selectionStart()
                cur.setPosition(og_end)
                cur.movePosition(QTextCursor.EndOfLine)
                end = cur.selectionEnd()

                cur.setPosition(start)
                cur.setPosition(end, QTextCursor.KeepAnchor)
                
                self.setTextCursor(cur)

                shift = False
                if event.modifiers() == Qt.ShiftModifier:
                    shift = True

                text = self.toPlainText()[start: end]
                tabs = 0
                lines = []
                for line in text.split('\n'):
                    if line:
                        if shift:
                            tabs -= 1
                            line = line.removeprefix('\t')
                        else:
                            tabs += 1
                            line = '\t' + line
                    lines.append(line)

                cur.insertText('\n'.join(lines))
                
                cur.setPosition(og_start)
                cur.setPosition(og_end, QTextCursor.KeepAnchor)
                self.setTextCursor(cur)

                cur.endEditBlock()
                event.ignore()
                return
            if event.text() in braces:
                start = cur.selectionStart()
                end = cur.selectionEnd()
                cur.beginEditBlock()
                cur.clearSelection()
                cur.setPosition(end)
                cur.insertText(braces[event.text()])
                cur.setPosition(start)
                cur.insertText(event.text())
                cur.setPosition(start + 1)
                cur.setPosition(end + 1, QTextCursor.KeepAnchor)
                self.setTextCursor(cur)
                cur.endEditBlock()
                return

        super().keyPressEvent(event)

        prefix = self.text_under_cursor()
        if event.key() == Qt.Key_Period:
            force_popup = True
        if prefix or force_popup:
            if self.model:
                self.model.set_prefix(prefix, self.textCursor())
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