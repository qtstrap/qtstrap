from qtstrap import *


class CodeEditor(QTextEdit):
    def __init__(self, *args, changed=None, model=None, highlighter=None, **kwargs):
        super().__init__(*args, **kwargs)

        self.braces = {
            '"': '"',
            "'": "'",
            '{': '}',
            '(': ')',
            '<': '>',
            '[': ']',
            '|': '|',
            '`': '`',
        }

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

        # ignore some keys when autocomplete popup is open
        keys = [Qt.Key_Enter, Qt.Key_Return, Qt.Key_Escape, Qt.Key_Tab, Qt.Key_Backtab]
        if self.completer.popup().isVisible():
            if event.key() in keys:
                event.ignore()
                return

        # comment or uncomment the selection
        if event.modifiers() == Qt.ControlModifier:
            if event.key() == Qt.Key_Slash:
                self.toggle_comments()
                event.accept()
                return

        # move the selection up or down
        if event.modifiers() == Qt.AltModifier:
            if event.key() == Qt.Key_Up:
                self.move_selection(-1)
                event.accept()
                return

            if event.key() == Qt.Key_Down:
                self.move_selection(1)
                event.accept()
                return

        cur = self.textCursor()
        # indent or dedent the selection
        if cur.hasSelection():
            if event.key() in [Qt.Key_Tab, Qt.Key_Backtab]:
                if event.modifiers() == Qt.ShiftModifier:
                    self.indent_selection(-1)
                else:
                    self.indent_selection(1)
                event.accept()
                return

        # wrap the selection with (), "", etc
        if cur.hasSelection():
            if event.text() in self.braces:
                self.wrap_selection(event.text())
                event.accept()
                return

        super().keyPressEvent(event)

        # handle autocomplete popup
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

    def expand_selection(self, cursor):
        pass

    def toggle_comments(self):
        cur = self.textCursor()
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

        text = self.toPlainText()[start: end]
        text_lines = text.split('\n')
        first_line = text_lines[0]
        og_length = len(text)
        lines = []
        
        add = not all([s[0] == '#' for s in text_lines if s])

        for line in text_lines:
            if line:
                if add:
                    line = '# ' + line
                else:
                    line = line.removeprefix('# ')
            lines.append(line)

        text = '\n'.join(lines)
        cur.insertText(text)

        final_end = og_end + len(text) - og_length
        final_start = og_start + len(lines[0]) - len(first_line)

        cur.setPosition(final_start)
        cur.setPosition(final_end, QTextCursor.KeepAnchor)
            
        self.setTextCursor(cur)
        cur.endEditBlock()

    def move_selection(self, direction):
        if direction == 1:
            direction = QTextCursor.Down
        if direction == -1:
            direction = QTextCursor.Up

        cur = self.textCursor()
        cur.beginEditBlock()

        og_start = cur.selectionStart()
        og_end = cur.selectionEnd()
        cur.setPosition(og_start)
        cur.movePosition(QTextCursor.StartOfLine)
        start = cur.selectionStart()
        cur.setPosition(og_end)
        cur.movePosition(QTextCursor.EndOfLine)
        end = cur.selectionEnd()

        if direction == QTextCursor.Up:
            cur.setPosition(start)
            cur.movePosition(QTextCursor.Up)
            cur.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            cur.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
            line = cur.selectedText()
            cur.setPosition(end)
            cur.movePosition(QTextCursor.Down)
            cur.movePosition(QTextCursor.StartOfLine)
            cur.insertText(line)
            cur.setPosition(start)
            cur.movePosition(QTextCursor.Up)
            cur.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            cur.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
            cur.removeSelectedText()
            cur.setPosition(og_start - len(line))
            cur.setPosition(og_end - len(line), QTextCursor.KeepAnchor)
            
        if direction == QTextCursor.Down:
            cur.setPosition(end)
            cur.movePosition(QTextCursor.Down, QTextCursor.KeepAnchor)
            cur.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            line = cur.selectedText()
            cur.setPosition(start)
            cur.movePosition(QTextCursor.Up)
            cur.movePosition(QTextCursor.EndOfLine)
            cur.insertText(line)
            cur.setPosition(end + len(line))
            cur.movePosition(QTextCursor.Down)
            cur.movePosition(QTextCursor.EndOfLine, QTextCursor.KeepAnchor)
            cur.movePosition(QTextCursor.Right, QTextCursor.KeepAnchor)
            cur.removeSelectedText()
            cur.setPosition(og_start + len(line))
            cur.setPosition(og_end + len(line), QTextCursor.KeepAnchor)

        self.setTextCursor(cur)
        cur.endEditBlock()

    def indent_selection(self, direction):
        cur = self.textCursor()
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

        text = self.toPlainText()[start: end]
        first_char = text[0]
        og_length = len(text)
        lines = []
        
        for line in text.split('\n'):
            if line:
                if direction == 1:
                    line = '\t' + line
                else:
                    line = line.removeprefix('\t')
            lines.append(line)

        text = '\n'.join(lines)
        cur.insertText(text)

        final_end = og_end + len(text) - og_length
        final_start = og_start

        if direction == 1:
            final_start = og_start + 1
        else:
            if first_char == '\t':
                final_start = og_start - 1

        cur.setPosition(final_start)
        cur.setPosition(final_end, QTextCursor.KeepAnchor)
            
        self.setTextCursor(cur)
        cur.endEditBlock()

    def wrap_selection(self, key):
        cur = self.textCursor()
        cur.beginEditBlock()

        start = cur.selectionStart()
        end = cur.selectionEnd()
        cur.clearSelection()
        cur.setPosition(end)
        cur.insertText(self.braces[key])
        cur.setPosition(start)
        cur.insertText(key)
        cur.setPosition(start + 1)
        cur.setPosition(end + 1, QTextCursor.KeepAnchor)

        self.setTextCursor(cur)
        cur.endEditBlock()

    def text(self):
        return self.toPlainText()