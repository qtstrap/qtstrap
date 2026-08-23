from qtstrap import *
from qtstrap.extras.promise import wait_for_signal


class AwaitableDialog(QDialog):
    """A dialog that can be awaited like a NiceGUI dialog.

    Usage:
        result = await ConfirmDialog()
        if result:
            do_thing()

    The dialog opens non-modally (open(), not exec()) so the async
    coroutine suspends without spinning a nested event loop.

    Call submit(result) from inside the dialog to resolve the await.
    Esc, X, or reject() resolves the await with None — no hang.
    """

    def __init__(self, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self._result = None

    def submit(self, result=None):
        """Resolve the dialog with a result value."""
        self._result = result
        self.accept()

    def __await__(self):
        # open() is non-modal — no nested event loop
        self.open()

        # Wait for the finished signal — fires for accept, reject, Esc, X
        yield from wait_for_signal(self.finished).__await__()

        self.deleteLater()
        return self._result