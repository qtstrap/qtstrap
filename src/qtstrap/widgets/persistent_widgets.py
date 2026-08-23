from qtstrap import *


class PersistentCheckBox(QCheckBox):
    def __init__(self, name, changed=None, model=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.model = model
        self.restore_state()

        if changed:
            self.stateChanged.connect(changed)

        self.stateChanged.connect(self._save_state)

    def _save_state(self):
        if self.model is not None:
            setattr(self.model, self.name, bool(self.checkState() == Qt.Checked))
        else:
            QSettings().setValue(self.name, int(self.checkState()))

    def restore_state(self):
        if self.model is not None:
            prev = getattr(self.model, self.name)
            if prev:
                self.setCheckState(Qt.Checked)
            return

        prev_state = QSettings().value(self.name, 0)
        try:
            prev_state = int(prev_state)
        except (TypeError, ValueError):
            return
        if prev_state == int(Qt.Checked):
            self.setCheckState(Qt.Checked)
        elif prev_state == int(Qt.PartiallyChecked):
            self.setCheckState(Qt.PartiallyChecked)

    def __bool__(self):
        return self.checkState() == Qt.Checked


class PersistentLineEdit(QLineEdit):
    def __init__(self, name, *args, default='', changed=None, model=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.default = default
        self.model = model
        self.restore_state()

        if changed:
            self.textChanged.connect(changed)

        self.textChanged.connect(self._save_state)

    def _save_state(self):
        if self.model is not None:
            setattr(self.model, self.name, self.text())
        else:
            QSettings().setValue(self.name, self.text())

    def restore_state(self):
        if self.model is not None:
            self.setText(str(getattr(self.model, self.name)))
            return
        self.setText(str(QSettings().value(self.name, self.default)))


class PersistentTextEdit(QTextEdit):
    def __init__(self, name, *args, default='', changed=None, model=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.default = default
        self.model = model
        self.restore_state()

        if changed:
            self.textChanged.connect(changed)

        self.textChanged.connect(self._save_state)

    def _save_state(self):
        if self.model is not None:
            setattr(self.model, self.name, self.toPlainText())
        else:
            QSettings().setValue(self.name, self.toPlainText())

    def restore_state(self):
        if self.model is not None:
            self.setText(str(getattr(self.model, self.name)))
            return
        self.setText(str(QSettings().value(self.name, self.default)))


class PersistentPlainTextEdit(QPlainTextEdit):
    def __init__(self, name, *args, default='', changed=None, model=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.default = default
        self.model = model
        self.restore_state()

        if changed:
            self.textChanged.connect(changed)

        self.textChanged.connect(self._save_state)

    def _save_state(self):
        if self.model is not None:
            setattr(self.model, self.name, self.toPlainText())
        else:
            QSettings().setValue(self.name, self.toPlainText())

    def restore_state(self):
        if self.model is not None:
            self.setPlainText(str(getattr(self.model, self.name)))
            return
        self.setPlainText(str(QSettings().value(self.name, self.default)))


class PersistentListWidget(QListWidget):
    def __init__(self, name, items=None, default=None, changed=None, model=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.default_selection = default or []
        self.model = model

        if items:
            self.addItems(items)
            self.restore_state()

        if changed:
            self.itemSelectionChanged.connect(changed)

        self.itemSelectionChanged.connect(self._save_state)

    def _save_state(self):
        value = self.selected_items()
        if self.model is not None:
            setattr(self.model, self.name, value)
        else:
            QSettings().setValue(self.name, value)

    def selected_items(self):
        return [item.text() for item in self.selectedItems()]

    def restore_state(self):
        if self.model is not None:
            prev_items = getattr(self.model, self.name) or []
        else:
            prev_items = QSettings().value(self.name, self.default_selection)
        if prev_items:
            if isinstance(prev_items, str):
                prev_items = [prev_items]
            for i in range(self.count()):
                if self.item(i).text() in prev_items:
                    self.item(i).setSelected(True)


class PersistentTreeWidget(QTreeWidget):
    def __init__(self, name, items=None, index_column=0, default=None, changed=None, model=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.default_selection = default or []
        self.index_column = index_column
        self.model = model

        if items:
            self.addItems(items)
            self.restore_state()

        if changed:
            self.itemSelectionChanged.connect(changed)

        self.itemSelectionChanged.connect(self._save_state)

    def _save_state(self):
        value = self.selected_items()
        if self.model is not None:
            setattr(self.model, self.name, value)
        else:
            QSettings().setValue(self.name, value)

    def selected_items(self):
        return [item.text(self.index_column) for item in self.selectedItems()]

    def restore_state(self):
        if self.model is not None:
            prev_items = getattr(self.model, self.name) or []
        else:
            prev_items = QSettings().value(self.name, self.default_selection)
        if prev_items:
            if isinstance(prev_items, str):
                prev_items = [prev_items]
            for i in range(self.count()):
                if self.item(i).text(self.index_column) in prev_items:
                    self.item(i).setSelected(True)


class PersistentComboBox(QComboBox):
    def __init__(self, name, items=None, changed=None, model=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.model = model

        if items:
            self.addItems(items)
            self.restore_state()

        if changed:
            self.currentTextChanged.connect(changed)

        self.currentTextChanged.connect(self._save_state)

    def _save_state(self):
        if self.model is not None:
            setattr(self.model, self.name, self.currentIndex())
        else:
            QSettings().setValue(self.name, self.currentIndex())

    def restore_state(self):
        if self.model is not None:
            try:
                self.setCurrentIndex(int(getattr(self.model, self.name)))
            except (TypeError, ValueError):
                pass
            return

        prev_index = QSettings().value(self.name, 0)
        try:
            prev_index = int(prev_index)
        except (TypeError, ValueError):
            return
        self.setCurrentIndex(prev_index)


class PersistentCheckableAction(QAction):
    def __init__(self, name, *args, model=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.model = model
        self.setCheckable(True)
        self.restore_state()

        self.triggered.connect(self._save_state)

    def _save_state(self):
        if self.model is not None:
            setattr(self.model, self.name, self.isChecked())
        else:
            QSettings().setValue(self.name, self.isChecked())

    def restore_state(self):
        if self.model is not None:
            if getattr(self.model, self.name):
                self.setChecked(True)
            return

        prev_state = QSettings().value(self.name, 0)
        if prev_state in (True, 'true', 1, '1'):
            self.setChecked(True)
        elif prev_state in (False, 'false', 0, '0'):
            self.setChecked(False)

    def __bool__(self):
        return self.isChecked()