from qtstrap import *


class PersistentCheckBox(QCheckBox):
    def __init__(self, name, changed=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.restore_state()

        if changed:
            self.stateChanged.connect(changed)

        self.stateChanged.connect(lambda: QSettings().setValue(self.name, self.checkState()))
    
    def restore_state(self):
        prev_state = QSettings().value(self.name, 0)
        if prev_state == int(Qt.Checked):
            self.setCheckState(Qt.Checked)
        elif prev_state == int(Qt.PartiallyChecked):
            self.setCheckState(Qt.PartiallyChecked)


class PersistentLineEdit(QLineEdit):
    def __init__(self, name, *args, default='', changed=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.default = default
        self.restore_state()

        if changed:
            self.textChanged.connect(changed)

        self.textChanged.connect(lambda: QSettings().setValue(self.name, self.text()))
    
    def restore_state(self):
        self.setText(str(QSettings().value(self.name, self.default)))


class PersistentTextEdit(QTextEdit):
    def __init__(self, name, *args, default='', changed=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.default = default
        self.restore_state()

        if changed:
            self.textChanged.connect(changed)

        self.textChanged.connect(lambda: QSettings().setValue(self.name, self.toPlainText()))
    
    def restore_state(self):
        self.setText(str(QSettings().value(self.name, self.default)))


class PersistentListWidget(QListWidget):
    def __init__(self, name, items=[], default=[], changed=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.default_selection = default

        if items:
            self.addItems(items)
            self.restore_state()
                
        if changed:
            self.itemSelectionChanged.connect(changed)

        self.itemSelectionChanged.connect(lambda: QSettings().setValue(self.name, self.selected_items()))

    def selected_items(self):
        return [item.text() for item in self.selectedItems()]

    def restore_state(self):
        prev_items = QSettings().value(self.name, self.default_selection)
        if prev_items:
            for i in range(self.count()):
                if self.item(i).text() in prev_items:
                    self.item(i).setSelected(True)


class PersistentTreeWidget(QTreeWidget):
    def __init__(self, name, items=[], index_column=0, default=[], changed=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.default_selection = default
        self.index_column = index_column

        if items:
            self.addItems(items)
            self.restore_state()
                
        if changed:
            self.itemSelectionChanged.connect(changed)

        self.itemSelectionChanged.connect(lambda: QSettings().setValue(self.name, self.selected_items()))

    def selected_items(self):
        return [item.text(self.index_column) for item in self.selectedItems()]

    def restore_state(self):
        prev_items = QSettings().value(self.name, self.default_selection)
        if prev_items:
            for i in range(self.count()):
                if self.item(i).text(self.index_column) in prev_items:
                    self.item(i).setSelected(True)


class PersistentComboBox(QComboBox):
    def __init__(self, name, items=[], changed=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name

        if items:
            self.addItems(items)
            self.restore_state()

        if changed:
            self.currentTextChanged.connect(changed)

        self.currentTextChanged.connect(lambda: QSettings().setValue(self.name, self.currentIndex()))

    def restore_state(self):
        prev_index = QSettings().value(self.name, 0)
        if isinstance(prev_index, int):
            self.setCurrentIndex(prev_index)


class PersistentCheckableAction(QAction):
    def __init__(self, name, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.setCheckable(True)
        self.restore_state()

        self.triggered.connect(lambda: QSettings().setValue(self.name, self.isChecked()))

    def restore_state(self):
        prev_state = QSettings().value(self.name, 0)
        if prev_state == 'true':
            self.setChecked(True)
        elif prev_state == 'false':
            self.setChecked(False)