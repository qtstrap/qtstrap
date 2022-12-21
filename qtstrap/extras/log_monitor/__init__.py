from .log_widget import LogMonitorWidget, LogMonitorDockWidget, LogMonitorDropdown
from .log_database_handler import DatabaseHandler
import logging
from qtstrap import OPTIONS
import sys


db_path = (OPTIONS.config_dir / 'log.db').as_posix()
exception_logger_name = 'exceptions'


def install(database_name=db_path, install_excepthook=False):
    logger = logging.getLogger()
    logger.setLevel(1)
    logger.addHandler(DatabaseHandler(database_name))

    exception_logger = logging.getLogger(exception_logger_name)
    def handle_exception(exc_type, exc_value, exc_traceback):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        exception_logger.error("Uncaught exception", exc_info=(exc_type, exc_value, exc_traceback))

    if install_excepthook:
        sys.excepthook = handle_exception