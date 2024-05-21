from qtstrap import (
    CHBoxLayout,
    CVBoxLayout,
    CGridLayout,
    CFormLayout,
    get_children,
)
from qtpy.QtCore import (
    QMargins,
)
from qtpy.QtWidgets import (
    QLabel,
    QWidget,
    QPushButton,
)


def test_context_layout():
    def get_hbox():
        with CHBoxLayout() as hbox:
            hbox.add(QLabel('H1'))
            hbox.add(QLabel('H2'))
        return hbox

    widget = QWidget()

    with CVBoxLayout(widget) as layout:
        layout.add(QLabel('test1'))
        layout += QLabel('test2')
        layout.add([QLabel('test3'), QLabel('test4')])
        layout += [QLabel('test5'), QLabel('test6')]
        layout.add(get_hbox())
        layout += get_hbox()
        test7 = layout + QLabel('test7')
        test8, test9 = layout + (QLabel('test8'), QLabel('test9'))

    assert len(get_children(widget)) == 16
    assert test7.text() == 'test7'


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


def test_form_layout():
    widget = QWidget()

    with CFormLayout(widget) as layout:
        # add() with two args
        layout.add('', QPushButton(''))
        # += tuple
        layout += ('', QPushButton(''))
        # += sequence of tuples
        layout += [('', QPushButton('')), ('', QPushButton(''))]
        # += dict
        layout += {'1': QPushButton(''), '2': QPushButton('')}

    assert len(get_children(widget)) == 9


def test_splitter():
    pass


def test_scrollarea():
    pass


def test_margins_formats():
    widget = QWidget()

    with CVBoxLayout(widget, margins=0) as layout:
        with layout.hbox(margins=(5, 5, 5, 5)) as layout:
            layout.add(QLabel('upper left'))
            layout.add(QLabel('upper right'))
        with layout.hbox(margins=QMargins(10, 10, 10, 10)) as layout:
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
