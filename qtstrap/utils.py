

def enable_children(thing):
    """ recursively walk the provided thing and enable all of its widget children """
    for i in range(thing.count()):
        if thing.itemAt(i).widget():
            thing.itemAt(i).widget().setEnabled(True)
        else:
            enable_children(thing.itemAt(i))


def disable_children(thing):
    """ recursively walk the provided thing and disable all of its widget children """
    for i in range(thing.count()):
        if thing.itemAt(i).widget():
            thing.itemAt(i).widget().setEnabled(False)
        else:
            disable_children(thing.itemAt(i))


def print_all_children(obj, prefix=''):
    for child in obj.children():
        print(prefix, child)
        print_all_children(child, '  ' + prefix )


def set_font_options(obj, options={}):
    font = obj.font()
    for setting, value in options.items():
        getattr(font, setting)(value)
    obj.setFont(font)
    return obj