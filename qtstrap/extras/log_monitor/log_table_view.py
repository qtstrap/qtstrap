from qtstrap import *
from qtpy.QtSql import *
import time
from .log_filter_controls import get_color
from .log_profile import LogProfile
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
                    return QColor(get_color(level[0]))
            except (IndexError, KeyError):
                pass
            return None
        elif role == Qt.ToolTipRole:                    # <- new lines
            return super().data(index, Qt.DisplayRole)  # <- new lines
        else:
            return super().data(index, role)


class LogTableView(QTableView):
    columns_changed = Signal()

    def __init__(self):
        super().__init__()
        self.setSelectionMode(QAbstractItemView.SingleSelection)
        self.verticalHeader().hide()
        self.verticalHeader().setDefaultSectionSize(12)

        header = self.horizontalHeader()
        header.setStretchLastSection(True)
        header.setContextMenuPolicy(Qt.CustomContextMenu)
        header.customContextMenuRequested.connect(self.header_menu)
        header.viewport().installEventFilter(self)

        self.db_model = LogDbModel(self)
        
        self.profile = LogProfile()

        self.setModel(self.db_model)
        self.need_to_refresh = False
        
        self.scan_timer = QTimer()
        self.scan_timer.timeout.connect(self.attempt_refresh)
        self.scan_timer.start(200)

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

    def set_columns(self, columns):
        self.profile.set_columns(columns)

    def refresh(self):
        at_bottom = False
        if self.verticalScrollBar().value() == self.verticalScrollBar().maximum():
            at_bottom = True

        db = QSqlDatabase.database(db_conn_name)

        query = db.exec_("SELECT COUNT(*) FROM 'log'")
        query.next()
        row_count = query.value(0)
        
        self.db_model.setQuery(self.profile.build_query(row_count), db)
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
            width = self.horizontalHeader().sectionSize(section)
            self.profile.visible_columns[section].width = width

        self.columns_changed.emit()

    def header_menu(self):
        menu = QMenu()

        for column in self.profile.columns:
            action = QAction(column.title, menu, checkable=True)
            action.setChecked(column.visible)
            action.triggered.connect(column.set_visibility)
            menu.addAction(action)

        if menu.exec_(QCursor.pos()):
            self.need_to_refresh = True
            self.columns_changed.emit()
            