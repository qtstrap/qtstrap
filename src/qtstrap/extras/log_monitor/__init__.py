import logging
import sys

from qtstrap import OPTIONS

from .log_database_handler import DatabaseHandler
from .log_widget import (
    LogMonitorDockWidget,
    LogMonitorDropdown,
    LogMonitorWidget,
)

exception_logger_name = 'exceptions'


def install(database_name=None, install_excepthook=True):
    if database_name is None:
        database_name = (OPTIONS.config_dir / 'log.db').as_posix()

    logger = logging.getLogger()
    logger.setLevel(1)
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
