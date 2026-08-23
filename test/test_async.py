"""Tests for the async signal/slot integration — promisify + qasync.

These tests verify that:
1. Sync handlers pass through _smart_connect with zero behavioral change
2. Async handlers connected via .connect() are eagerly scheduled as tasks
3. wait_for_signal resolves with signal arguments
4. Promise combinators (all/race/any) work under qasync
5. owned_by cancels a promise when the owner QObject is destroyed
6. promisify wraps both sync and async functions correctly
"""
import asyncio
import sys

import pytest
from qtpy.QtCore import QObject, Signal, QTimer, Qt
from qtpy.QtWidgets import QApplication, QPushButton, QLabel

from qtstrap.extras._qasync import QEventLoop
from qtstrap.extras.promise import Promise, promisify, wait_for_signal, owned_by


def run_async(coro_factory, timeout_s=5.0):
    """Run a coroutine under qasync with a hard timeout.

    Returns the coroutine's result or raises the exception.
    """
    results = []

    async def runner():
        try:
            result = await coro_factory()
            results.append(('ok', result))
        except Exception as e:
            results.append(('err', e))
        # Schedule quit
        QApplication.quit()

    loop = QEventLoop(QApplication.instance())
    asyncio.set_event_loop(loop)
    with loop:
        loop.run_until_complete(runner())

    if not results:
        raise TimeoutError('qasync loop did not complete')
    kind, value = results[0]
    if kind == 'err':
        raise value
    return value


@pytest.fixture(autouse=True)
def qapp(qtbot):
    yield qtbot


# --- Section 1: _smart_connect passthrough ---


def test_sync_handler_passes_through(qtbot):
    """Sync signal handlers should work identically with _smart_connect."""
    received = []

    button = QPushButton()
    button.clicked.connect(lambda: received.append('clicked'))

    qtbot.mouseClick(button, Qt.LeftButton)
    assert received == ['clicked']


# --- Section 2: Async handler via .connect() ---


def test_async_handler_runs():
    """An async def connected to a signal should run as a task under qasync."""
    label = QLabel('before')

    async def on_click():
        await asyncio.sleep(0.01)
        label.setText('after')

    button = QPushButton()
    button.clicked.connect(on_click)

    async def main():
        button.click()
        await asyncio.sleep(0.1)
        assert label.text() == 'after'

    run_async(main)


def test_async_handler_with_arguments():
    """Async handler should receive signal arguments."""
    results = []

    class Emitter(QObject):
        sig = Signal(int, str)

    emitter = Emitter()

    async def handler(num, text):
        await asyncio.sleep(0.01)
        results.append((num, text))

    emitter.sig.connect(handler)

    async def main():
        emitter.sig.emit(42, 'hello')
        await asyncio.sleep(0.1)
        assert results == [(42, 'hello')]

    run_async(main)


# --- Section 3: wait_for_signal ---


def test_wait_for_signal_single_arg():
    """wait_for_signal should resolve with the signal's argument."""
    class Emitter(QObject):
        sig = Signal(str)

    emitter = Emitter()

    async def main():
        QTimer.singleShot(10, lambda: emitter.sig.emit('result'))
        result = await wait_for_signal(emitter.sig)
        assert result == 'result'

    run_async(main)


def test_wait_for_signal_zero_args():
    """wait_for_signal with a zero-arg signal should resolve with None."""
    class Emitter(QObject):
        sig = Signal()

    emitter = Emitter()

    async def main():
        QTimer.singleShot(10, lambda: emitter.sig.emit())
        result = await wait_for_signal(emitter.sig)
        assert result is None

    run_async(main)


def test_wait_for_signal_multi_args():
    """wait_for_signal with multi-arg signal should resolve with a tuple."""
    class Emitter(QObject):
        sig = Signal(int, str)

    emitter = Emitter()

    async def main():
        QTimer.singleShot(10, lambda: emitter.sig.emit(42, 'hello'))
        result = await wait_for_signal(emitter.sig)
        assert result == (42, 'hello')

    run_async(main)


def test_wait_for_signal_timeout():
    """wait_for_signal should raise TimeoutError on timeout."""
    class Emitter(QObject):
        sig = Signal()

    emitter = Emitter()

    async def main():
        try:
            await wait_for_signal(emitter.sig, timeout=0.05)
            assert False, 'should have timed out'
        except asyncio.TimeoutError:
            pass  # expected

    run_async(main)


# --- Section 4: Promise combinators ---


def test_promise_all():
    """Promise.all should resolve with all results in order."""
    @promisify
    async def slow(value, delay):
        await asyncio.sleep(delay)
        return value

    async def main():
        results = await Promise.all([
            slow('a', 0.03),
            slow('b', 0.01),
            slow('c', 0.02),
        ])
        assert results == ['a', 'b', 'c']

    run_async(main)


def test_promise_race():
    """Promise.race should resolve with the first settled promise."""
    @promisify
    async def slow(value, delay):
        await asyncio.sleep(delay)
        return value

    async def main():
        result = await Promise.race([
            slow('slow', 0.1),
            slow('fast', 0.01),
        ])
        assert result == 'fast'

    run_async(main)


def test_promise_then_catch_chain():
    """Promise.then/catch should chain correctly."""
    @promisify
    async def fails():
        await asyncio.sleep(0.01)
        raise ValueError('boom')

    async def main():
        result = await fails().catch(lambda e: f'caught: {e}')
        assert 'caught: boom' in result

def test_owned_by_cancels_on_destroy():
    """owned_by should cancel a promise when the owner is destroyed."""
    owner = QObject()

    async def long_running():
        await asyncio.sleep(10)
        return 'should not get here'

    async def main():
        promise = promisify(long_running)()
        owned_by(promise, owner)
        owner.deleteLater()
        await asyncio.sleep(0.1)
        assert promise.cancelled() or promise.future.cancelled()

    run_async(main)


# --- Section 6: promisify wraps sync functions ---


def test_promisify_sync_function():
    """promisify should work on plain sync functions."""
    @promisify
    def add(a, b):
        return a + b

    promise = add(1, 2)
    assert isinstance(promise, Promise)


def test_promisify_sync_function_awaitable():
    """A promisified sync function should be awaitable under qasync."""
    @promisify
    def add(a, b):
        return a + b

    async def main():
        result = await add(3, 4)
        assert result == 7

    run_async(main)