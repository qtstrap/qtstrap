from .options import *
from .settings import *
from .qt import *
from .utils import *
from .layouts import *
from .widgets import *
from .base_application import BaseApplication
from .base_window import BaseMainWindow
from .toolbar import BaseToolbar, SettingsToolbar
from .timestamp import TimeStamp, time_since


# create a shorter alias for accessing the current QApplication
App = QApplication.instance