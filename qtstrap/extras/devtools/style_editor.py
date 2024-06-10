from qtstrap import *
from monaco import MonacoWidget


class StyleEditorDockWidget(BaseDockWidget):
    _title = 'Style Editor'
    _starting_area = Qt.BottomDockWidgetArea
    _shortcut = 'Ctrl+Y'

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        prev_text = QSettings().value('custom_style', '')

        self.editor = MonacoWidget()
        self.editor.setText(prev_text)
        self.editor.setLanguage('css')
        self.editor.setTheme('vs-dark')
        self.editor.textChanged.connect(lambda t: QSettings().setValue('custom_style', t))

        with CVBoxLayout(self._widget, margins=2) as layout:
            layout.add(self.editor)
            with layout.hbox():
                layout.add(QLabel(), 1)
                layout.add(QPushButton('Apply', clicked=self.apply))

    def apply(self):
        text = self.editor.text()
        self.parent().setStyleSheet(text)
