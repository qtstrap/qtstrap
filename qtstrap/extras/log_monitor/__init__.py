from .log_widget import LogMonitorWidget, LogMonitorDockWidget, LogMonitorDropdown
from .log_database_handler import DatabaseHandler
import logging
from qtstrap import OPTIONS


db_path = OPTIONS.config_dir + '/log.db'


def install(database_name=db_path):
    logger = logging.getLogger()
    logger.setLevel(1)
    logger.addHandler(DatabaseHandler(database_name))