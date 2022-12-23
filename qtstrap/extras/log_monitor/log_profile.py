import time


session_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - 1))


class Column:
    def __init__(self, title=None, query=None, visible=True, width=0):
        self.title = title
        self.query = query if query else title
        self.default_visiblity = visible
        self.visible = visible
        self.default_width = width
        self.width = width

    def set_visibility(self, visible):
        self.visible = visible

    def set_data(self, data):
        self.visible = data.get('visible', self.default_visiblity)
        self.width = data.get('width', self.default_width)

    def get_data(self):
        data = {}

        if self.default_width:
            if self.default_width != self.width:
                data['width'] = self.width
        if self.default_visiblity != self.visible:
            data['visible'] = self.visible
        
        return data


default_columns = [
    Column("Time", "TimeStamp", width=130, visible=True),
    Column("'Level#'", "LogLevel", width=40, visible=False),
    Column("Level", "LogLevelName", width=60, visible=True),
    Column("Source", width=200, visible=True),
    Column("Module", width=100, visible=False),
    Column("'Module:Func:Line'", "Module || ':' || FuncName || ':' || LineNo", width=120, visible=False),
    Column("'Func:Line'", "FuncName || ':' || LineNo", width=120, visible=True),
    Column("Func", "FuncName", width=120, visible=False),
    Column("Line", "LineNo", width=40, visible=False),
    Column("Args", width=100, visible=False),
    Column("Exception", width=100, visible=False),
    Column("Process", width=100, visible=False),
    Column("Thread", width=100, visible=False),
    Column("ThreadName", width=100, visible=False),
    Column("Message", visible=True),
]


class LogProfile:
    def __init__(self):
        self.columns = default_columns

        self.loggers = {
            'global': ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
        }
        self.visible_loggers = ['global']
        self.text_filter = ''
        self.current_session_only = True
        self.query_limit = 1000

    @property
    def visible_columns(self):
        return [c for c in self.columns if c.visible]

    @property
    def column_data(self):
        return {c.title: c.get_data() for c in self.columns if c.get_data()}

    def get_log_level_column(self):
        return [c.title for c in self.visible_columns].index('Level')

    def set_filter(self, filt):
        self.text_filter = filt['text']
        self.visible_loggers = filt['visible_loggers']
        self.loggers = filt['loggers']
        self.current_session_only = filt['current_session_only']
        self.query_limit = filt['query_limit']

    def set_columns(self, column_data):
        for c in self.columns:
            c.set_data(column_data.get(c.title, {}))

    def build_query(self, row_count):
        query = "SELECT "

        columns = []
        for col in self.columns:
            if col.visible:
                if col.title != col.query:
                    columns.append(f'{col.query} AS {col.title}')
                else:
                    columns.append(f'{col.title}')

        query += ', '.join(columns)
        query += " FROM 'log'"

        where = []
        if self.current_session_only:
            where.append(f"TimeStamp > '{session_start_time}'")

        if self.query_limit:
            where.append(f"rowid > {row_count - self.query_limit}")

        if self.text_filter:
            where.append(f"Message LIKE '%{self.text_filter}%'")
        
        if self.visible_loggers:
            sources = []
            for logger in self.visible_loggers:
                levels = ', '.join([f'"{l}"' for l in self.loggers[logger]])
                s = f'(Source = "{logger}" AND LogLevelName IN ({levels}))'
                sources.append(s)
            
            where.append(f"({' OR '.join(sources)})")

        if where:
            query += ' WHERE ' + ' AND '.join(where)

        return query
