from .log_widget import LogMonitorWidget, LogMonitorDockWidget, LogMonitorDropdown


from .log_database_handler import DatabaseHandler
import logging


def install(database_name):
    logger = logging.getLogger()
    logger.setLevel(1)
    logger.addHandler(DatabaseHandler(database_name))