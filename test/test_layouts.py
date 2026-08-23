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


def test_splitter(qtbot):
    from qtstrap import CSplitter, PersistentCSplitter
    from qtpy.QtWidgets import QLabel

    widget = QWidget()
    qtbot.addWidget(widget)

    with CVBoxLayout(widget) as layout:
        with layout.split() as splitter:
            splitter.add(QLabel('left'))
            splitter.add(QLabel('right'))
            assert splitter._layout.count() == 2

    # PersistentCSplitter should also work
    widget2 = QWidget()
    qtbot.addWidget(widget2)

    with CVBoxLayout(widget2) as layout:
        with layout.split('test_persistent_splitter') as splitter:
            splitter.add(QLabel('a'))
            splitter.add(QLabel('b'))
            assert splitter._layout.count() == 2


def test_scrollarea(qtbot):
    from qtstrap import CScrollArea, PersistentCScrollArea
    from qtpy.QtWidgets import QLabel

    # CScrollArea: children should land in the inner widget's layout
    widget = QWidget()
    qtbot.addWidget(widget)

    with CVBoxLayout(widget) as layout:
        with layout.scroll() as scroll:
            for i in range(50):
                scroll.add(QLabel(f'label {i}'))
            # scroll is a ContextLayout; scroll._layout is the CScrollArea on the stack
            inner_layout = scroll._layout.widget().layout()
            assert inner_layout.count() == 50

    # PersistentCScrollArea: should also accept children and persist scroll position
    widget2 = QWidget()
    qtbot.addWidget(widget2)

    with CVBoxLayout(widget2) as layout:
        with layout.scroll('test_persistent_scroll') as scroll:
            for i in range(10):
                scroll.add(QLabel(f'item {i}'))
            inner_layout = scroll._layout.widget().layout()
            assert inner_layout.count() == 10


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
