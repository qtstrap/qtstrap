from qtstrap import *
import typing
from style import colors
import re


class CommandRegistry(QObject):
    def __init__(self) -> None:
        self.registry = {}
        self.commands = []

    def register_command(self, command):
        self.registry[command.text()] = command
        self.commands.append(command)
        self.commands.sort(key=lambda x: x.text())

    def execute(self, command_name):
        self.registry[command_name].triggered.emit()


registry = CommandRegistry()


class Command(QAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        registry.register_command(self)

        self.usage_count = 0
        self.triggered.connect(self.used)
    
    def used(self):
        self.usage_count += 1


class PopupDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.prefix = ""
        self.normal = QPen('gray')
        self.contains = QPen('lightgray')
        self.highlight = QPen(QColor(colors.blue))

    def set_prefix(self, prefix):
        self.prefix = prefix

    def paint(self, 
            painter: PySide2.QtGui.QPainter, 
            option: PySide2.QtWidgets.QStyleOptionViewItem, 
            index: PySide2.QtCore.QModelIndex
        ):

        self.initStyleOption(option, index)
        prefix = self.prefix
        value = index.data(Qt.EditRole)
        shortcut = index.data(Qt.UserRole)

        # adjust full drawing area
        option.rect.setX(option.rect.x() + 5)
        option.rect.setWidth(option.rect.width() - 10)

        painter.save()

        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, QColor('#243F89'))

        if prefix == "":
            painter.setPen(self.normal)
            painter.drawText(option.rect, Qt.AlignLeft, value)
        else:
            if prefix.lower() in value.lower():
                parts = re.split(prefix, value, flags=re.IGNORECASE)
                
                # the split is case insensitive, so use the lengths of the
                # parts to slice the original text out of the complete string
                sections = [parts[0]]
                length = len(parts[0])
                for part in parts[1:]:
                    sections.append(value[length:length + len(prefix)])
                    sections.append(part)
                    length += len(prefix) + len(part)

                prev = None
                rect = QRect(option.rect)
                for text in sections:
                    if text.lower() == prefix.lower():
                        painter.setPen(self.highlight)
                    else:
                        painter.setPen(self.contains)

                    if prev:
                        rect = QRect(prev.x() + prev.width(), prev.y(), option.rect.width(), prev.height())

                    prev = painter.drawText(rect, Qt.AlignLeft, text)
            else:
                painter.setPen(self.normal)
                painter.drawText(option.rect, Qt.AlignLeft, value)

        painter.setPen(self.normal)
        painter.drawText(option.rect, Qt.AlignRight, shortcut)

        painter.restore()


class CommandModel(QAbstractListModel):
    sorted_commands = []

    def sort_commands(self, prefix):
        self.sorted_commands = [cmd for cmd in registry.commands if prefix.lower() in cmd.text().lower()]
        result = bool(self.sorted_commands)
        self.sorted_commands.extend([cmd for cmd in registry.commands if prefix.lower() not in cmd.text().lower()])
        return result

    def rowCount(self, parent: PySide2.QtCore.QModelIndex) -> int:
        return len(registry.commands)

    def data(self, index: PySide2.QtCore.QModelIndex, role: int) -> typing.Any:
        if not index.isValid():
            return None

        if role == Qt.EditRole:
            return self.sorted_commands[index.row()].text()
        
        elif role == Qt.UserRole:
            return self.sorted_commands[index.row()].shortcut().toString()

    def index(self, row: int, column: int, parent: PySide2.QtCore.QModelIndex) -> PySide2.QtCore.QModelIndex:
        return self.createIndex(row, column)


class CommandCompleter(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.list = QListView()
        self.list.setUniformItemSizes(True)
        self.list.setSelectionRectVisible(True)
        self.list.setSelectionMode(QAbstractItemView.SingleSelection)
        self.list.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.list.setFixedHeight(500)

        self.command_model = CommandModel(self)
        self.list.setModel(self.command_model)

        self.delegate = PopupDelegate(self)
        self.list.setItemDelegate(self.delegate)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.list)
        self.active = False

    def open(self):
        self.active = True
        self.update_prefix('')
        super().show()

    def close(self):
        self.active = False
        self.update_prefix('')
        super().hide()

    def update_prefix(self, prefix):
        self.delegate.set_prefix(prefix)
        self.command_model.sort_commands(prefix)

        index = self.list.model().index(0, 0, QModelIndex())
        self.list.setCurrentIndex(index)
        
        # redraw items in popup
        for row in range(self.list.model().rowCount(QModelIndex())):
            index = self.list.model().index(row, 0, QModelIndex())
            self.list.update(index)

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


class _CommandPalette(QDialog):
    _instance = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName('CommandPalette')
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFocusPolicy(Qt.StrongFocus)
        
        set_font_options(self, {'setPointSize': 16})
        
        self.setMinimumWidth(700)

        self.action = QAction("Command Palette", self)
        self.action.setShortcut('Ctrl+Shift+P')
        self.action.triggered.connect(self.palette)

        self.line = QLineEdit()
        self.line.setStyleSheet("""
            QLineEdit {
                font-size: 16pt;
                border: 1px solid #0074D9;
            }
        """)
        self.command_completer = CommandCompleter(self)

        self.line.textChanged.connect(self.command_completer.update_prefix)
        self.line.returnPressed.connect(self.accept)
        self.command_completer.list.clicked.connect(self.accept)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.addWidget(self.line)
        layout.addWidget(self.command_completer)

        self.command_completer.close()

        self.installEventFilter(self)
        self.line.installEventFilter(self)
        self.callback = None

    def palette(self):
        self.open()
        self.command_completer.open()

    def _open(self, cb=None, prompt=None, placeholder=None, completer=None, validator=None, mask=None):
        self.callback = cb

        self.line.setText(prompt)
        self.line.setPlaceholderText(placeholder)
        self.line.setCompleter(completer)
        self.line.setValidator(validator)
        self.line.setInputMask(mask)

        self.center_on_parent()
        self.show()
        self.activateWindow()
        self.line.setFocus()

    def open(self, cb=None, prompt=None, placeholder=None, completer=None, validator=None, mask=None):
        QTimer.singleShot(0, lambda: self._open(cb, prompt, placeholder, completer, validator, mask))

    def accept(self):
        if self.command_completer.active:
            name = self.command_completer.get_selection()
            self.dismiss()
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
        r = self.parent().frameGeometry()
        rect = QRect(r.x() - (self.width() / 2), r.y(), r.width(), 100)
        self.move(rect.center())


def CommandPalette(parent=None):
    if _CommandPalette._instance is None:
        _CommandPalette._instance = _CommandPalette(parent)

    return _CommandPalette._instance