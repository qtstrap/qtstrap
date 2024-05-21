from qtstrap import *


class BindableCheckAction(QAction):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setCheckable(True)

    #     self.restore_state()

    # self.triggered.connect(lambda: QSettings().setValue(self.name, self.isChecked()))

    # def restore_state(self):
    #     prev_state = QSettings().value(self.name, 0)
    #     if prev_state == 'true':
    #         self.setChecked(True)
    #     elif prev_state == 'false':
    #         self.setChecked(False)

    def bind(self, obj, attribute: str):
        self.triggered.connect(lambda: setattr(obj, attribute, self.isChecked()))

        state = getattr(obj, attribute)
        if state == 'true':
            self.setChecked(True)
        elif state == 'false':
            self.setChecked(False)

        return self

    def __bool__(self):
        return self.isChecked()
