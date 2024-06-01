from qtstrap import *
from qtstrap.extras.style import qcolors
from qtpy.shiboken import isValid, delete
import qtawesome as qta
from .inspector import Inspector


try:
    from qtstrap.extras.command_palette import CommandPalette, Command

    command_palette_available = True
except:
    command_palette_available = False


class SceneTreeDelegate(QStyledItemDelegate):
    def __init__(self):
        super().__init__()

        self.label = QLabel()
        self.doc = QtGui.QTextDocument()

    def paint(self, painter, option, index):
        self.initStyleOption(option, index)
        text = index.data(Qt.DisplayRole)

        if text is None:
            super().paint(painter, option, index)
            return

        r = QRect(option.rect)
        bg_rect = QRect(r.x() - 3, r.y(), r.width() + 3, r.height())

        if option.state & QStyle.State_MouseOver:
            brush = QBrush(QColor('#e5f3ff'))
            painter.fillRect(QRect(bg_rect), brush)
        if option.state & QStyle.State_Selected:
            if option.state & QStyle.State_Active:
                brush = QBrush(QColor('#cde8ff'))
            elif option.state & QStyle.State_MouseOver:
                brush = QBrush(QColor('#cde8ff'))
            else:
                brush = QBrush(QColor('#d9d9d9'))
            painter.fillRect(QRect(bg_rect), brush)

            if option.state & QStyle.State_MouseOver:
                painter.setPen(QColor('#99d1ff'))
                r = QRect(bg_rect)
                painter.drawLine(r.topLeft(), r.topRight())
                painter.drawLine(r.bottomLeft(), r.bottomRight())
                painter.drawLine(r.topLeft(), r.bottomLeft())

        painter.save()

        parts = text.split('<')
        parts[1] = '<' + parts[1]

        rect = QRect(option.rect)

        if parts[0]:
            painter.setPen(qcolors.white)
            prev = painter.drawText(rect, Qt.AlignLeft, parts[0])
            rect = QRect(prev.x() + prev.width(), prev.y(), option.rect.width(), prev.height())
        else:
            painter.setPen(qcolors.gray)
            painter.drawText(rect, Qt.AlignLeft, parts[1])

        painter.restore()


class SceneTreeWidgetItem(QTreeWidgetItem):
    def __init__(self, parent, node):
        super().__init__(parent)

        self.node = node
        self.obj = node.obj

        obj = node.obj

        name = obj.objectName()
        klass = type(obj).__name__

        s = ''
        if name:
            s += f'{name} '

        s += f'<{klass}>'

        self.setText(0, s)

        self.update_visibility_icon()

    def update_visibility_icon(self):
        if isinstance(self.obj, QWidget):
            if self.obj.isVisible():
                self.setIcon(1, qta.icon('fa5.eye'))
            else:
                self.setIcon(1, qta.icon('fa5.eye-slash'))

    def toggle_visibility(self):
        if isinstance(self.obj, QWidget):
            if self.obj.isVisible():
                self.obj.hide()
            else:
                self.obj.show()

            self.update_visibility_icon()


class TreeNode(QObject):
    inverse = {}

    def __init__(self, obj=None, parent=None, item_parent=None):
        super().__init__()
        self.obj = obj
        self.parent = parent
        self._children = []
        self.item = SceneTreeWidgetItem(item_parent, self)

        self.inverse[obj] = self

        self.obj.installEventFilter(self)
        # self.obj.destroyed.connect(self.obj_destroyed)

    def eventFilter(self, watched, event) -> bool:
        if not isValid(self.item):
            return False

        if event.type() in (QEvent.Show, QEvent.Hide):
            self.item.update_visibility_icon()

        if event.type() == QEvent.ChildAdded:
            new_obj = event.child()
            if isinstance(new_obj, (QWidget, QLayout)):
                self.scan()

        return False

    def obj_destroyed(self, obj):
        if obj in self.inverse:
            node = self.inverse[obj]
            if isValid(node.item):
                node.item.parent().removeChild(node.item)
                delete(node.item)

            self.inverse.pop(obj)

    def scan(self):
        for child_obj in self.obj.children():
            if child_obj in self.inverse:
                continue
            if isinstance(child_obj, TreeNode):
                continue
            if isinstance(child_obj, (QWidget, QLayout)):
                node = TreeNode(obj=child_obj, parent=self, item_parent=self.item)
                self._children.append(node)
                node.scan()


class SceneTree(QTreeWidget):
    inspection_requested = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setItemDelegate(SceneTreeDelegate())
        self.setColumnCount(2)
        self.header().hide()
        self.header().setMinimumSectionSize(1)
        self.header().setStretchLastSection(False)
        self.header().setSectionResizeMode(0, QHeaderView.Stretch)

        for i in range(1, 2):
            self.setColumnWidth(i, 30)

        self.itemClicked.connect(self.click)
        self.itemDoubleClicked.connect(self.double_click)
        self.itemSelectionChanged.connect(self.selection_changed)

    def click(self, item, column):
        if column == 0:
            self.inspection_requested.emit(item)
        if column == 1:
            item.toggle_visibility()

    def double_click(self, item, column):
        pass

    def selection_changed(self):
        pass

    def contextMenuEvent(self, event):
        pos = event.globalPos()
        item = self.itemAt(self.viewport().mapFromGlobal(pos))
        menu = QMenu()

        if isinstance(item.obj, QWidget):
            if item.obj.isVisible():
                menu.addAction('Hide').triggered.connect(item.toggle_visibility)
            else:
                menu.addAction('Show').triggered.connect(item.toggle_visibility)

        menu.addAction('Open REPL')
        menu.addAction('Edit Style')

        menu.exec_(pos)

    def scan(self, obj):
        self.clear()
        self.root_node = TreeNode(obj=obj, item_parent=self)
        self.root_node.scan()
        self.root_node.item.setExpanded(True)


class SceneTreeWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.tree = SceneTree()
        self.inspector = Inspector()

        self.tree.inspection_requested.connect(self.inspector.inspect)

        with PersistentCSplitter('scene_tree_splitter', self) as splitter:
            splitter.add(self.tree)
            splitter.add(self.inspector)


class SceneTreeDockWidget(BaseDockWidget):
    _title = 'Scene Tree'
    _starting_area = Qt.LeftDockWidgetArea
    _shortcut = 'Ctrl+L'

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.scene_tree = SceneTreeWidget(self)
        self.setWidget(self.scene_tree)

        if command_palette_available:
            self.commands = [
                Command('Scene Tree: Show scene tree', triggered=self.show),
                Command('Scene Tree: Hide scene tree', triggered=self.hide),
            ]

        call_later(lambda: self.scene_tree.tree.scan(self.parent()), 2000)
