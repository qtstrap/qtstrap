from .qt import QSettings
from .options import *


class PortableSettings(QSettings):
    settings_file_path = 'settings.ini'

    def __init__(self, *args, **kwargs):
        super().__init__(
            self.settings_file_path,
            QSettings.IniFormat,
            *args,
            **kwargs
        )

    @staticmethod
    def _install():
        PortableSettings.settings_file_path = (
            OPTIONS.PORTABLE_SETTINGS_FILE.as_posix()
        )