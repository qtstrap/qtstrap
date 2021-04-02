import sys

def uncache(exclude):
    """Remove package modules from cache except excluded ones.
    On next import they will be reloaded.
    
    Args:
        exclude (iter<str>): Sequence of module paths.
    """
    pkgs = []
    for mod in exclude:
        pkg = mod.split('.', 1)[0]
        pkgs.append(pkg)

    to_uncache = []
    for mod in sys.modules:
        if mod in exclude:
            continue

        if mod in pkgs:
            to_uncache.append(mod)
            continue

        for pkg in pkgs:
            if mod.startswith(pkg + '.'):
                to_uncache.append(mod)
                break

    for mod in to_uncache:
        del sys.modules[mod]


from pathlib import Path


if Path('.portable').exists():
    print('patching QSettings')
    from PySide2 import QtCore

    class PortableSettings(QtCore.QSettings):
        def __init__(self, *args, **kwargs):
            super().__init__('settings.ini', QtCore.QSettings.IniFormat, *args, **kwargs)

    QtCore.QSettings = PortableSettings
    uncache(['QtCore'])