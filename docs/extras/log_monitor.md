# Log Monitor

The log monitor system redirects application logs to an SQLite3 database for persistence. Also registers a global `sys.excepthook`, and logs all uncaught exceptions.

## `LogMonitorWidget`

A very powerful log monitor widget that connects to the local log database, providing a live view of application logs.

Store multiple profiles of advanced filters:
- text filter
- query limit
- limit to current application session
- individually enable/disable log sources
- individually enable/disable every log level of every source


## `LogMonitorDockWidget`

a `LogMonitorWidget` wrapped in a `QDockWidget`


## `LogMonitorDropdown`

a `LogMonitorWidget` wrapped in an application-covering drop down panel


Installing the log monitor:

```py
from qtstrap import *
from qtstrap.extras import log_monitor


# give a custom name to the uncaught exception handler
log_monitor.exception_logger_name = 'your_application.exceptions'

# install the log handler
log_monitor.install()


class MainWindow(BaseMainWindow):
    def __init__(self, parent=None) -> None:
        super().__init__(parent=parent)

        # create an instance of the dropdown version of the log monitor
        self.log_monitor = log_monitor.LogMonitorDropdown(self, shortcut='ctrl+`')

        # create a statusbar, which contains a settings button and a settings menu
        self.create_statusbar()

        # add the log monitor's toggle view action to the settings menu
        self.settings_menu.addAction(self.log_monitor.toggleViewAction())
        

```