import logging
import sys

from qtstrap import OPTIONS

from .async_database_handler import AsyncDatabaseHandler, DatabaseHandler
from .log_widget import (
    LogMonitorDockWidget,
    LogMonitorDropdown,
    LogMonitorWidget,
)

exception_logger_name = 'exceptions'


def install(database_name=None, install_excepthook=True, use_async=True):
    """
    Install the log monitor handler.
    
    Args:
        database_name: Path to SQLite database file (default: OPTIONS.config_dir/log.db)
        install_excepthook: Whether to install exception handler (default: True)
        use_async: Use async non-blocking handler (default: True)
    """
    if database_name is None:
        database_name = (OPTIONS.config_dir / 'log.db').as_posix()

    logger = logging.getLogger()
    logger.setLevel(1)
    
    if use_async:
        logger.addHandler(AsyncDatabaseHandler(database_name))
    else:
        logger.addHandler(DatabaseHandler(database_name))

    exception_logger = logging.getLogger(exception_logger_name)

    if install_excepthook:
        _excepthook = sys.excepthook

        def handle_exception(exc_type, exc_value, exc_traceback):
            module = exc_traceback.tb_frame.f_code.co_filename
            lineno = exc_traceback.tb_lineno
            funcName = exc_traceback.tb_frame.f_code.co_name

            msg = f'[{module}:{lineno}, in {funcName}] {exc_type.__name__} {exc_value}'

            exception_logger.error(msg, exc_info=(exc_type, exc_value, exc_traceback))
            _excepthook(exc_type, exc_value, exc_traceback)

        sys.excepthook = handle_exception
