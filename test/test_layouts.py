from qtstrap import *


def test_context_layout():
    widget = QWidget()

    with CVBoxLayout(widget) as layout:
        layout.add(QLabel('test'))

    assert len(get_children(widget)) == 2


def test_nested_context_layout():
    widget = QWidget()

    with CVBoxLayout(widget) as layout:
        with layout.hbox() as layout:
            layout.add(QLabel('upper left'))
            layout.add(QLabel('upper right'))
        with layout.hbox() as layout:
            layout.add(QLabel('lower left'))
            layout.add(QLabel('lower right'))

    assert len(get_children(widget)) == 7