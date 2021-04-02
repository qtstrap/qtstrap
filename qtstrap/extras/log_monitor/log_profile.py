import time


session_start_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


class Column:
    def __init__(self, name=None, title=None, visible=True, width=50):
        self.name = name
        self.title = title if title else name
        self.visible = visible
        self.width = width

    def set_visibility(self, visible):
        self.visible = visible


default_columns = [
    Column("TimeStamp", "Time", width=150, visible=True),
    Column("Source", width=200, visible=True),
    Column("LogLevel", "Level#", width=100, visible=False),
    Column("LogLevelName", "Level", width=80, visible=True),
    Column("Message", width=100, visible=True),
    Column("Args", width=100, visible=False),
    Column("Module", width=100, visible=False),
    Column("FuncName", "Func", width=100, visible=False),
    Column("LineNo", "Line", width=100, visible=False),
    Column("Exception", width=100, visible=False),
    Column("Process", width=100, visible=False),
    Column("Thread", width=100, visible=False),
    Column("ThreadName", width=100, visible=False),
]


class LogProfile:
    def __init__(self):
        self.columns = default_columns

        self.loggers = {
            'global': ['DEBUG','INFO','WARNING','ERROR','CRITICAL'],
        }
        self.visible_loggers = ['global']
        self.text_filter = ''
        self.current_session_only = True
        self.query_limit = 1000

    @property
    def visible_columns(self):
        return [c for c in self.columns if c.visible]

    def get_log_level_column(self):
        return [c.name for c in self.visible_columns].index('LogLevelName')

    def set_filter(self, filt):
        self.text_filter = filt['text']
        self.visible_loggers = filt['visible_loggers']
        self.loggers = filt['loggers']
        self.current_session_only = filt['current_session_only']
        self.query_limit = filt['query_limit']

    def build_query(self):
        query = "SELECT "

        columns = []
        for col in self.columns:
            if col.visible:
                if col.name != col.title:
                    columns.append(f'"{col.name}" AS "{col.title}"')
                else:
                    columns.append(f'"{col.name}"')

        query += ', '.join(columns)
        query += " FROM 'log'"

        where = []
        if self.current_session_only:
            where.append(f"TimeStamp > '{session_start_time}'")

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
            query += f' WHERE ' + ' AND '.join(where)
        
        if self.query_limit:
            query += f" LIMIT {self.query_limit}"

        return query