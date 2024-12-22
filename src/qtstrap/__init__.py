# Copyright (c) 2022, David Kincaid


from .options import *

try:
    from .qt import *
except ModuleNotFoundError as e:
    raise ModuleNotFoundError('No Qt Bindings found. Try "uv add PySide6" or "pip install PySide6"') from e
else:
    from .settings import PortableSettings

    if OPTIONS.portable:
        from .settings import PortableSettings as QSettings

        QSettings._install()

    from .base_application import BaseApplication
    from .base_window import (
        BaseMainWindow,
        ThemeMenu,
    )
    from .utils import *
    from .widgets import *

    # create a shorter alias for accessing the current QApplication
    App = QApplication.instance
