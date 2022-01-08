from qtstrap import *
from qtpy.QtSql import *
from .log_table_view import LogTableView
from .log_filter_controls import FilterControls
from .log_database_handler import DatabaseHandler, db_conn_name


try:
    from command_palette import CommandPalette, Command
    command_palette_available = True
except:
    command_palette_available = False


class LogMonitorWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.tab_name = "Log Monitor"

        if command_palette_available:
            self.commands = [
                Command("Log Monitor: Switch profile", triggered=self.open_profile_prompt),
            ]

        self.log_table = LogTableView()
        DatabaseHandler.register_callback(self.log_table.schedule_refresh)

        self.filter_controls = FilterControls()
        self.filter_controls.filter_updated.connect(self.log_table.set_filter)
        self.filter_controls.update_filter()

        self.query_existing_loggers()

        with PersistentCSplitter('log_monitor_splitter', self) as splitter:
            splitter.add(self.filter_controls, 1)
            splitter.add(self.log_table, 10)

    def open_profile_prompt(self):
        profiles = list(self.filter_controls.settings['profiles'].keys())

        self.completer = QCompleter(self, profiles)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)
        self.completer.setCompletionMode(QCompleter.PopupCompletion)

        QTimer.singleShot(0, lambda: CommandPalette().open(
            placeholder='Select a profile',
            cb=lambda result: print(result),
            completer=self.completer
        ))

    def query_existing_loggers(self):
        db = QSqlDatabase.database(db_conn_name)
        query = db.exec_("SELECT Source FROM 'log'")
        loggers = set()
        while query.next():
            loggers.add(query.value(0))
        self.filter_controls.logger_filter.register_loggers(loggers)


class LogMonitorDockWidget(QDockWidget):
    def __init__(self, parent=None):
        super().__init__('Log Monitor', parent=parent)
        self.setObjectName('LogMonitor')

        self.setWidget(LogMonitorWidget(self))

        if command_palette_available:
            self.commands = [
                Command("Log Monitor: Show log monitor", triggered=self.show, shortcut='Ctrl+L'),
                Command("Log Monitor: Hide log monitor", triggered=self.hide),
            ]

        self.setAllowedAreas(Qt.AllDockWidgetAreas)
        self.dockLocationChanged.connect(lambda: QTimer.singleShot(0, self.adjust_size))

        self.starting_area = Qt.BottomDockWidgetArea

        if not self.parent().restoreDockWidget(self):
            self.parent().addDockWidget(self.starting_area, self)
        
        self.closeEvent = lambda x: self.hide()

    def adjust_size(self):
        if self.isFloating():
            self.adjustSize()
            
    def toggleViewAction(self):
        action = super().toggleViewAction()
        action.setShortcut('Ctrl+L')
        return action


class LogMonitorDropdown(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setWindowFlags(Qt.Tool | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setFocusPolicy(Qt.StrongFocus)

        CHBoxLayout(self).add(LogMonitorWidget(self))
        
        if command_palette_available:
            self.commands = [
                Command("Log Monitor: Show log monitor", triggered=self.show, shortcut='Ctrl+L'),
                Command("Log Monitor: Hide log monitor", triggered=self.hide),
            ]
        
        self.hide()

    def toggleViewAction(self):
        action = QAction("Toggle Log Monitor", self)
        action.setShortcut('`')
        action.triggered.connect(self.toggle_view)
        return action

    def toggle_view(self):
        if self.isVisible():
            self.hide()
        else:
            self.center_on_parent()
            self.show()

    def center_on_parent(self):
        offset = 33
        r = self.parent().frameGeometry()
        rect = QRect(r.x(), r.y() + offset, r.width(), r.height() - (offset * 2))
        self.setGeometry(rect)