from asyncio import Event

from qtpy.QtWidgets import QDialog


class AwaitableDialog(QDialog):
    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)

        self._result = None
        self._submitted = Event()

    def submit(self, result=None):
        self._result = result
        self._submitted.set()

    def __await__(self):
        self.show()

        # block until the Event gets set
        # reference: https://github.com/zauberzeug/nicegui/blob/main/nicegui/elements/dialog.py#L45
        yield from self._submitted.wait().__await__()

        self.close()
        self.deleteLater()

        return self._result
