"""Tests for AwaitableDialog — the NiceGUI-style awaitable dialog."""
import asyncio

import pytest
from qtpy.QtCore import Qt, QTimer
from qtpy.QtWidgets import QPushButton, QLabel

from qtstrap import *
from qtstrap.extras._qasync import QEventLoop
def run_async(coro_factory):
    results = []

    app = QApplication.instance() or QApplication([])

    async def runner():
        try:
            result = await coro_factory()
            results.append(('ok', result))
        except Exception as e:
            results.append(('err', e))
        QApplication.quit()

    loop = QEventLoop(QApplication.instance())
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(runner())

    if not results:
        raise TimeoutError('loop did not complete')
    kind, value = results[0]
    if kind == 'err':
        raise value
    return value


class ConfirmDialog(AwaitableDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Confirm')

        self.label = QLabel('Are you sure?')
        self.yes_btn = QPushButton('Yes')
        self.no_btn = QPushButton('No')

        self.yes_btn.clicked.connect(lambda: self.submit(True))
        self.no_btn.clicked.connect(lambda: self.submit(False))

        with CVBoxLayout(self) as layout:
            layout.add(self.label)
            with layout.hbox(align='center'):
                layout.add(self.yes_btn)
                layout.add(self.no_btn)


def test_awaitable_dialog_submit_true():
    """Awaiting a dialog should return the submitted value."""
    async def main():
        dialog = ConfirmDialog()
        QTimer.singleShot(10, lambda: dialog.yes_btn.click())
        result = await dialog
        assert result is True

    run_async(main)


def test_awaitable_dialog_submit_false():
    """Submit with False should return False."""
    async def main():
        dialog = ConfirmDialog()
        QTimer.singleShot(10, lambda: dialog.no_btn.click())
        result = await dialog
        assert result is False

    run_async(main)


def test_awaitable_dialog_reject_returns_none():
    """Esc or reject() should resolve with None, not hang."""
    async def main():
        dialog = ConfirmDialog()
        QTimer.singleShot(10, lambda: dialog.reject())
        result = await dialog
        assert result is None

    run_async(main)


def test_awaitable_dialog_default_none():
    """A dialog that never calls submit should still resolve on close."""
    async def main():
        dialog = AwaitableDialog()
        dialog.setWindowTitle('test')
        QTimer.singleShot(10, lambda: dialog.reject())
        result = await dialog
        assert result is None

    run_async(main)