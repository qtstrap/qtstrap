from qtstrap import QSettings
from pydantic import BaseModel, ConfigDict, field_validator, ValidationInfo


model_state = {}


class SettingsModel(BaseModel):
    model_config = ConfigDict(validate_assignment=True)

    def __init__(self):
        model_state[type(self).__name__] = False
        super().__init__()
        self.load_settings()

    def load_settings(self):
        model_state[type(self).__name__] = False
        for name, field in self.model_fields.items():
            value = QSettings().value(f'{self.Config.prefix}/{name}', field.default)
            setattr(self, name, value)

        model_state[type(self).__name__] = True

    @field_validator('*')
    @classmethod
    def autosave(cls, value, info: ValidationInfo):
        if model_state[cls.__name__]:
            QSettings().setValue(f'{cls.Config.prefix}/{info.field_name}', value)
        return value
