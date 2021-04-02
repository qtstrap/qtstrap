from qtstrap import *
from qtpy.QtSql import *
import time
from .log_filter_controls import log_levels
from .log_profile import LogProfile, Column, default_columns
from .log_database_handler import db_conn_name


session_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class LogDbModel(QSqlQueryModel):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.log_level_column = 2

    def data(self, index, role=Qt.DisplayRole):
        if role == Qt.ForegroundRole:
            try:
                if index.column() == self.log_level_column:
                    level = super().data(index, Qt.DisplayRole)
                    return QColor(log_levels[level])
            except (IndexError, KeyError):
                pass
            return None
        else:
            return super().data(index, role)


class LogTableView(QTableView):
    def __init__(self):
        super().__init__()
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(12)

        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setContextMenuPolicy(Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(self.header_menu)
        header.setSectionsMovable(True)
        header.viewport().installEventFilter(self)

        self.db_model = LogDbModel(self)
        
        self.profile = LogProfile()

        self.setModel(self.db_model)
        self.need_to_refresh = False
        
        self.scan_timer = QTimer()
        self.scan_timer.timeout.connect(self.attempt_refresh)
        self.scan_timer.start(250)

    def attempt_refresh(self):
        if self.need_to_refresh:
            self.db_model.log_level_column = self.profile.get_log_level_column()
            self.refresh()
            self.need_to_refresh = False

    def schedule_refresh(self):
        self.need_to_refresh = True

    def set_filter(self, filt):
        self.profile.set_filter(filt)
        self.refresh()

    def refresh(self):
        at_bottom = False
        if self.verticalScrollBar().value() == self.verticalScrollBar().maximum():
            at_bottom = True
        
        self.db_model.setQuery(self.profile.build_query(), QSqlDatabase.database(db_conn_name))
        while self.db_model.canFetchMore():
            self.db_model.fetchMore()

        for i, column in enumerate(self.profile.visible_columns):
            self.horizontalHeader().resizeSection(i, column.width)

        if at_bottom:
            self.scrollToBottom()

    def eventFilter(self, object, event):
        if event.type() == QEvent.MouseButtonRelease:
            self.mouse_released()
            return True
        return False

    def mouse_released(self):
        for section in range(self.horizontalHeader().count()):
            col = self.profile.visible_columns[section]
            col.width = self.horizontalHeader().sectionSize(section)

    def header_menu(self):
        menu = QMenu()

        for column in self.profile.columns:
            action = QAction(column.title, menu, checkable=True)
            action.setChecked(column.visible)
            action.triggered.connect(column.set_visibility)
            menu.addAction(action)

        if menu.exec_(QCursor.pos()):
            self.need_to_refresh = True