from qtstrap import *


class Widget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.button = QPushButton('button')
        self.label = QLabel('label')

        with CVBoxLayout(self) as layout:
            layout.add(self.button)
            layout.add(self.label)


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.button = QPushButton('button')
        self.label = QLabel('label')
        self.widget = Widget()

        with CVBoxLayout(self) as layout:
            layout.add(self.button)
            layout.add(self.label)
            layout.add(self.widget)


def test_enable_and_disable_children(qtbot):
    window = MainWindow()
    
    # children should start enabled
    assert window.button.isEnabled() == True
    assert window.label.isEnabled() == True
    assert window.widget.button.isEnabled() == True
    assert window.widget.label.isEnabled() == True

    disable_children(window)
    assert window.button.isEnabled() == False
    assert window.label.isEnabled() == False
    assert window.widget.button.isEnabled() == False
    assert window.widget.label.isEnabled() == False

    enable_children(window)
    assert window.button.isEnabled() == True
    assert window.label.isEnabled() == True
    assert window.widget.button.isEnabled() == True
    assert window.widget.label.isEnabled() == True

    disable_children(window.widget)
    assert window.button.isEnabled() == True
    assert window.label.isEnabled() == True
    assert window.widget.button.isEnabled() == False
    assert window.widget.label.isEnabled() == False

    enable_children(window.widget)
    assert window.button.isEnabled() == True
    assert window.label.isEnabled() == True
    assert window.widget.button.isEnabled() == True
    assert window.widget.label.isEnabled() == True


def test_get_all_children(qtbot):
    widget = Widget()
    children = get_children(widget)

    # this Widget should have 3 children: a layout, a pushbutton, and a label
    assert len(children) == 3
    assert type(children[0]) == CVBoxLayout
    assert type(children[1]) == QPushButton
    assert type(children[2]) == QLabel


def test_set_font_options(qtbot):
    window = MainWindow()
    
    # default font size is 8
    assert window.label.font().pointSize() == 8
    assert window.label.font().bold() == False

    set_font_options(window, {'setPointSize': 12, 'setBold': True})

    assert window.label.font().pointSize() == 12
    assert window.label.font().bold() == True