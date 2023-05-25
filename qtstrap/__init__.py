# Copyright (c) 2022, David Kincaid

import sys
from pathlib import Path


try:
    import pretty_errors
except:
    pass


from .options import *


if Path(sys.argv[0]).parts[-1] != 'qtstrap':
    try:
        from .qt import *
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError(
            'No Qt Bindings found. Try "pip install PySide6" or "pip install PySide6"'
        ) from e
    else:
        from .settings import PortableSettings
        
        if OPTIONS.portable:
            from .settings import PortableSettings as QSettings
            QSettings._install()

        from .settings_model import SettingsModel

        from .utils import *
        from .widgets import *
        from .base_application import (
            BaseApplication,
            install_app_info,
            install_ctrlc_handler,
        )
        from .base_window import (
            BaseMainWindow,
            ThemeMenu,
        )

        # create a shorter alias for accessing the current QApplication
        App = QApplication.instance
