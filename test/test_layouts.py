from qtstrap import (
    CVBoxLayout,
    CGridLayout,
    get_children
)
from qtpy.QtWidgets import (
    QLabel,
    QWidget,
)

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


def test_cgridlayout_helper_params():
    with CVBoxLayout() as vbox:
        vbox.add(QLabel('1'))
        vbox.add(QLabel('2'))

    widget = QWidget()

    with CGridLayout(widget) as layout:
        layout.add(QLabel('old'), 0, 0, 1, 2)
        layout.add(QLabel('new'), 1, 0, rowSpan=1, columnSpan=2)

        layout.add(QLabel('duplicate'), 2, 0, 1, 2, rowSpan=1, columnSpan=2)
        layout.add(QLabel('only one'), 3, 0, rowSpan=2)
        layout.add(QLabel('one of each'), 4, 0, 1, columnSpan=2)

        layout.add(vbox, 5, 0, 1, 2)

    assert len(get_children(widget)) == 9
