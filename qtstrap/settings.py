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


try:
    from .qt import QtCore

    class PortableSettings(QtCore.QSettings):
        settings_file_path = 'settings.ini'

        def __init__(self, *args, **kwargs):
            super().__init__(
                self.settings_file_path,
                QtCore.QSettings.IniFormat,
                *args,
                **kwargs
            )

        @staticmethod
        def _install():
            QtCore.QSettings = PortableSettings
            uncache(['QtCore'])

    from qtstrap.options import OPTIONS

    if OPTIONS.portable:
        PortableSettings.settings_file_path = (
            OPTIONS.PORTABLE_SETTINGS_FILE.as_posix()
        )
        PortableSettings._install()
except:
    pass
