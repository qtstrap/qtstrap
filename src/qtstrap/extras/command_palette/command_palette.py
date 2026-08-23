from qtstrap import *
import typing
import time


class CommandRegistry(QObject):
    def __init__(self) -> None:
        super().__init__()
        self.registry = {}
        self.commands = []

    def register_command(self, command):
        self.registry[command.text()] = command
        self.commands.append(command)
        self.commands.sort(key=lambda x: x.text())

    def unregister_command(self, name):
        if name in self.registry:
            del self.registry[name]
            cmd = next((c for c in self.commands if c.text() == name), None)
            if cmd:
                self.commands.remove(cmd)

    def execute(self, command_name):
        self.registry[command_name].triggered.emit()


registry = CommandRegistry()


class Command(QAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        registry.register_command(self)

        # Load frecency data from QSettings
        self.usage_count = int(QSettings().value(f'command_palette/{self.text()}/count', 0))
        self.last_used = float(QSettings().value(f'command_palette/{self.text()}/last_used', 0))
        self.triggered.connect(self.used)

        # Auto-unregister when the command is destroyed
        text = self.text()
        self.destroyed.connect(lambda _=None: registry.unregister_command(text))

    def used(self):
        self.usage_count += 1
        self.last_used = time.time()
        QSettings().setValue(f'command_palette/{self.text()}/count', self.usage_count)
        QSettings().setValue(f'command_palette/{self.text()}/last_used', self.last_used)

class PopupDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.prefix = ''

    def get_colors(self):
        palette = QApplication.palette()
        
        # Normal text color from palette
        self.normal = QPen(palette.color(QPalette.WindowText))
        
        # Selected item text
        self.selected = QPen(QColor('#FFFFFF'))
        
        # Text that matches search prefix - use same as normal
        self.contains = QPen(self.normal.color())
        
        # Highlighted match color (cyan stands out on muted background)
        self.highlight = QPen(QColor('#00d4ff'))
        
        # Selection background - desaturated to let cyan matches stand out
        if palette.color(QPalette.Window).lightness() < 128:
            self.background = QColor('#3d4f5f')  # Muted blue-gray for dark theme
        else:
            self.background = QColor('#b0c4d1')  # Muted blue-gray for light theme

    def set_prefix(self, prefix):
        self.prefix = prefix

    def paint(
        self,
        painter: QtGui.QPainter,
        option: QtWidgets.QStyleOptionViewItem,
        index: QtCore.QModelIndex,
    ):

        self.initStyleOption(option, index)
        prefix = self.prefix
        value = index.data(Qt.EditRole)
        shortcut = index.data(Qt.UserRole)
        selected = option.state & QStyle.State_Selected

        # adjust full drawing area
        option.rect.setX(option.rect.x() + 5)
        option.rect.setWidth(option.rect.width() - 10)

        painter.save()

        if selected:
            painter.fillRect(option.rect, self.background)

        if prefix == '':
            if selected:
                painter.setPen(self.selected)
            else:
                painter.setPen(self.normal)
            painter.drawText(option.rect, Qt.AlignLeft, value)
        else:
            if prefix.lower() in value.lower():
                parts = re.split(re.escape(prefix), value, flags=re.IGNORECASE)

                # the split is case insensitive, so use the lengths of the
                # parts to slice the original text out of the complete string
                sections = [parts[0]]
                length = len(parts[0])
                for part in parts[1:]:
                    sections.append(value[length : length + len(prefix)])
                    sections.append(part)
                    length += len(prefix) + len(part)

                prev = None
                rect = QRect(option.rect)
                for text in sections:
                    if text.lower() == prefix.lower():
                        painter.setPen(self.highlight)
                    else:
                        if selected:
                            painter.setPen(self.selected)
                        else:
                            painter.setPen(self.normal)

                    if prev:
                        rect = QRect(
                            prev.x() + prev.width(),
                            prev.y(),
                            option.rect.width(),
                            prev.height(),
                        )

                    prev = painter.drawText(rect, Qt.AlignLeft, text)
            else:
                if selected:
                    painter.setPen(self.selected)
                else:
                    painter.setPen(self.normal)
                painter.drawText(option.rect, Qt.AlignLeft, value)

        painter.setPen(self.normal)
        painter.drawText(option.rect, Qt.AlignRight, shortcut)

        painter.restore()


class CommandModel(QAbstractListModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.sorted_commands = []
        self._source = []

    def set_source(self, items):
        """Set the source list. Items can be QAction objects (command mode)
        or plain strings (option picker mode)."""
        self._source = items
        self.sort_commands('')

    def _frecency_score(self, item):
        """Score by frequency + recency. Higher = more relevant."""
        count = getattr(item, 'usage_count', 0)
        last_used = getattr(item, 'last_used', 0)
        if count == 0:
            return 0
        # Recency decay: score halves every 24 hours
        age = time.time() - last_used
        recency = 1.0 / (1.0 + age / 86400.0)
        return count * recency

    def sort_commands(self, prefix):
        self.beginResetModel()
        if prefix:
            matched = [item for item in self._source if prefix.lower() in self._item_text(item).lower()]
            unmatched = [item for item in self._source if prefix.lower() not in self._item_text(item).lower()]
            # Sort matched by frecency (most used/recent first), then alphabetically
            matched.sort(key=lambda item: (-self._frecency_score(item), self._item_text(item).lower()))
            self.sorted_commands = matched + unmatched
        else:
            # No prefix: sort all by frecency, then alphabetically
            self.sorted_commands = sorted(self._source, key=lambda item: (-self._frecency_score(item), self._item_text(item).lower()))
        self.endResetModel()
        return bool(self.sorted_commands)

    def _item_text(self, item):
        return item.text() if hasattr(item, 'text') else str(item)

    def rowCount(self, parent: QtCore.QModelIndex) -> int:
        return len(self.sorted_commands)

    def data(self, index: QtCore.QModelIndex, role: int) -> typing.Any:
        if not index.isValid():
            return None

        item = self.sorted_commands[index.row()]

        if role == Qt.EditRole:
            return self._item_text(item)

        elif role == Qt.UserRole:
            if hasattr(item, 'shortcut'):
                return item.shortcut().toString()
            return ''

    def index(self, row: int, column: int, parent: QtCore.QModelIndex) -> QtCore.QModelIndex:
        return self.createIndex(row, column)

class CommandCompleter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.active = False
        self.delegate = PopupDelegate(self)

        self.list = QListView()
        self.list.setUniformItemSizes(True)
        self.list.setSelectionRectVisible(True)
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setResizeMode(QListView.Adjust)
        self.list.setItemDelegate(self.delegate)

        self.command_model = CommandModel(self)
        self.list.setModel(self.command_model)

        with CVBoxLayout(self, margins=0) as layout:
            layout.add(self.list)

    def reset(self):
        self.delegate.get_colors()

    def open(self, source=None):
        self.active = True
        if source is not None:
            self.command_model.set_source(source)
        else:
            self.command_model.set_source(registry.commands)
        self.update_prefix('')
        super().show()

    def close(self):
        self.active = False
        self.update_prefix('')
        super().hide()

    def update_prefix(self, prefix):
        self.delegate.set_prefix(prefix)
        self.command_model.sort_commands(prefix)

    def move_selection_up(self):
        current = self.list.currentIndex()

        if current.row() > 0:
            new = self.list.model().index(current.row() - 1, 0, QModelIndex())
            self.list.setCurrentIndex(new)

    def move_selection_down(self):
        current = self.list.currentIndex()

        if current.row() < self.list.model().rowCount(QModelIndex()) - 1:
            new = self.list.model().index(current.row() + 1, 0, QModelIndex())
            self.list.setCurrentIndex(new)

    def get_selection(self):
        index = self.list.currentIndex()
        return index.data(Qt.EditRole)


@singleton
class CommandPalette(QDialog):
    def __init__(self, parent=None, shortcut='Ctrl+Shift+P'):
        super().__init__(parent)
        self.setObjectName('CommandPalette')
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFocusPolicy(Qt.StrongFocus)

        set_font_options(self, {'setPointSize': 16})

        self.setMinimumWidth(700)

        self.shortcut = shortcut

        self.action = QAction('Command Palette', self)
        self.action.setShortcut(self.shortcut)
        self.action.triggered.connect(self.palette)

        self.line = QLineEdit()
        # self.line.setStyleSheet("""
        #     QLineEdit {
        #         font-size: 16pt;
        #         border: 1px solid #0074D9;
        #     }
        # """)
        self.command_completer = CommandCompleter(self)

        self.line.textChanged.connect(self.command_completer.update_prefix)
        self.line.returnPressed.connect(self.accept)
        self.command_completer.list.clicked.connect(self.accept)

        with CVBoxLayout(self, margins=(5, 5, 5, 5)) as layout:
            layout.add(self.line)
            layout.add(self.command_completer)

        self.command_completer.close()

        self.installEventFilter(self)
        self.line.installEventFilter(self)
        self.callback = None

    def palette(self):
        self.open()
        self.command_completer.open()

    def _open(
        self,
        cb=None,
        prompt=None,
        placeholder=None,
        choices=None,
        completer=None,
        validator=None,
        mask=None,
    ):
        self.callback = cb

        self.line.setText(prompt)
        self.line.setPlaceholderText(placeholder)
        self.line.setCompleter(completer)
        self.line.setValidator(validator)
        self.line.setInputMask(mask)

        if choices is not None:
            self.command_completer.open(source=choices)
        else:
            self.command_completer.close()

        self.command_completer.reset()
        self.center_on_parent()
        self.show()
        self.activateWindow()
        self.line.setFocus()

    def open(
        self,
        cb=None,
        prompt=None,
        placeholder=None,
        choices=None,
        completer=None,
        validator=None,
        mask=None,
    ):
        QTimer.singleShot(
            0,
            lambda: self._open(cb, prompt, placeholder, choices, completer, validator, mask),
        )

    def accept(self):
        if self.command_completer.active:
            name = self.command_completer.get_selection()
            self.dismiss()
            if self.callback:
                # Option picker mode — return selection to callback
                self.callback(name)
            else:
                # Command mode — execute the command
                registry.execute(name)
        else:
            result = self.line.text()
            if self.callback:
                self.callback(result)
            self.dismiss()

    def dismiss(self):
        self.callback = None
        self.line.clear()
        self.line.setPlaceholderText('')
        self.line.setCompleter(None)
        self.line.setValidator(None)
        self.line.setInputMask('')
        self.hide()
        self.command_completer.close()

    def eventFilter(self, source, event):
        if event.type() == QEvent.KeyPress:
            if event.key() == Qt.Key_Return:
                self.accept()

            if source is not self:
                if self.command_completer.active:
                    if event.key() == Qt.Key_Up:
                        event.accept()
                        self.command_completer.move_selection_up()
                        return True

                    elif event.key() == Qt.Key_Down:
                        event.accept()
                        self.command_completer.move_selection_down()
                        return True

            if event.key() == QtCore.Qt.Key_Escape:
                self.dismiss()
                event.accept()
                return True

        if event.type() == QEvent.WindowDeactivate:
            self.dismiss()
            event.accept()
            return True

        return False

    def center_on_parent(self):
        parent = self.parent()
        if parent is not None:
            r = parent.frameGeometry()
        else:
            screen = QApplication.primaryScreen()
            if screen is None:
                return
            r = screen.availableGeometry()
        rect = QRect(r.x() - (self.width() / 2), r.y(), r.width(), 100)
        self.move(rect.center())
