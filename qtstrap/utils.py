from qtstrap import *


def enable_children(thing):
    """
    Recursively walk the provided thing and enable all of its widget children.
    """
    # QMainWindows don't have children, they have a centralWidget
    if isinstance(thing, QMainWindow):
        thing = thing.centralWidget()

    # QWidgets don't have children, they have a layout that has children
    if isinstance(thing, QWidget):
        thing = thing.layout()

    for i in range(thing.count()):
        if thing.itemAt(i).widget():
            thing.itemAt(i).widget().setEnabled(True)
        else:
            enable_children(thing.itemAt(i))


def disable_children(thing):
    """
    Recursively walk the provided thing and disable all of its widget children.
    """
    # QMainWindows don't have children, they have a centralWidget
    if isinstance(thing, QMainWindow):
        thing = thing.centralWidget()

    # QWidgets don't have children, they have a layout that has children
    if isinstance(thing, QWidget):
        thing = thing.layout()

    for i in range(thing.count()):
        if thing.itemAt(i).widget():
            thing.itemAt(i).widget().setEnabled(False)
        else:
            disable_children(thing.itemAt(i))


def print_children(obj, prefix=''):
    """
    Recursively visit all the children of the specified object and print them.
    """
    for child in obj.children():
        print(prefix, child)
        print_children(child, '  ' + prefix )


def set_font_options(obj, options={}):
    font = obj.font()
    for setting, value in options.items():
        getattr(font, setting)(value)
    obj.setFont(font)
    return obj