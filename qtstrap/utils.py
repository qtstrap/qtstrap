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


def get_children(obj) -> list[QObject]:
    """
    Recursively visit all the children of the specified object and collect them in a list.
    """
    children = []

    def _get_children(obj, prefix=''):
        for child in obj.children():
            children.append(child)
            _get_all_children(child, '  ' + prefix )

    _get_all_children(obj)

    return children


def print_children(obj, prefix=''):
    """
    Recursively visit all the children of the specified object and print them.
    """
    for child in obj.children():
        print(prefix, child)
        print_children(child, '  ' + prefix )


def set_font_options(obj, options={}):
    """
    Set the QFont options of the specified object.
    Font options are specified by providing the name of the QFont setter method.
    
    Example:
    set_font_options(widget, {'setPointSize': 12, 'setBold': True})

    is equivalent to writing:
    font = widget.font()
    font.setPointSize(12)
    font.setBold(True)
    widget.setFont(font)
    """
    font = obj.font()
    for setting, value in options.items():
        getattr(font, setting)(value)
    obj.setFont(font)
    return obj