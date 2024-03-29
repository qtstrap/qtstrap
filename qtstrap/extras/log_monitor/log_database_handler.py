import logging
from qtstrap import *
from qtpy.QtSql import *
import time


db_conn_name = 'logs'


initial_sql = """
CREATE TABLE IF NOT EXISTS log(
    TimeStamp TEXT,
    Source TEXT,
    LogLevel INT,
    LogLevelName TEXT,
    Message TEXT,
    Args TEXT,
    Module TEXT,
    FuncName TEXT,
    LineNo INT,
    Exception TEXT,
    Process INT,
    Thread TEXT,
    ThreadName TEXT
)
"""

insertion_sql = """
INSERT INTO log(
    TimeStamp,
    Source,
    LogLevel,
    LogLevelName,
    Message,
    Args,
    Module,
    FuncName,
    LineNo,
    Exception,
    Process,
    Thread,
    ThreadName
)
VALUES (
    '%(dbtime)s',
    '%(name)s',
    %(levelno)d,
    '%(levelname)s',
    '%(msg)s',
    '%(args)s',
    '%(module)s',
    '%(funcName)s',
    %(lineno)d,
    '%(exc_text)s',
    %(process)d,
    '%(thread)s',
    '%(threadName)s'
);
"""


class DatabaseHandler(logging.Handler):
    callbacks = []

    """A logging.Handler subclass that redirects outbound records to a local sqlite3 database """

    def __init__(self, database_name):
        super().__init__()
        self.formatter = logging.Formatter('%(asctime)s')

        db = QSqlDatabase.addDatabase('QSQLITE', db_conn_name)
        db.setDatabaseName(database_name)
        db.open()
        db.exec_(initial_sql)

    def format_time(self, record):
        record.dbtime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created))

    def emit(self, record):
        self.format(record)
        self.format_time(record)

        # single quotes need to be escaped in an SQL query
        record.msg = record.msg.replace("'", "''")

        if record.exc_info:
            record.exc_text = logging._defaultFormatter.formatException(record.exc_info).replace("'", "''")
        else:
            record.exc_text = ''

        # Insert the log record
        db = QSqlDatabase.database(db_conn_name)

        query_string = insertion_sql % record.__dict__
        result = db.exec_(query_string)
        # if db.lastError().isValid():
        #     print(db.lastError())
        #     print(query_string)
        #     print(result.executedQuery())

        for cb in self.callbacks:
            cb()

    @classmethod
    def register_callback(cls, cb):
        cls.callbacks.append(cb)

    def write(self, m):
        pass
