from qtstrap import QSettings
from pydantic import BaseModel, validator


model_state = {}


class SettingsModel(BaseModel):
    class Config:
        validate_assignment = True

    def __init__(self):
        model_state[type(self).__name__] = False
        super().__init__()
        self.load_settings()

    def load_settings(self):
        model_state[type(self).__name__] = False
        prefix = self.Config.prefix
        for name, field in self.__fields__.items():
            value = QSettings().value(f'{prefix}/{name}', field.default)
            setattr(self, name, value)

        model_state[type(self).__name__] = True

    @validator('*')
    def autosave(cls, value, field):
        if model_state[cls.__name__]:
            QSettings().setValue(f'{cls.Config.prefix}/{field.name}', value)
        return value
