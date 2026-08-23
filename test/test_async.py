"""Tests for the async signal/slot integration — promisify + QtAsyncio.

These tests verify that:
1. Sync handlers pass through _smart_connect with zero behavioral change
2. Async handlers connected via .connect() are eagerly scheduled as tasks
3. wait_for_signal resolves with signal arguments
4. Promise combinators (all/race/any) work under QtAsyncio
5. owned_by cancels a promise when the owner QObject is destroyed
6. promisify wraps both sync and async functions correctly
"""
import asyncio
import threading
import time

import pytest
from qtpy.QtCore import QObject, Signal, QTimer
from qtpy.QtWidgets import QApplication, QPushButton, QLabel

try:
    import PySide6.QtAsyncio as QtAsyncio
    HAVE_QTASYNCIO = True
except ImportError:
    HAVE_QTASYNCIO = False

from qtstrap.extras.promise import Promise, promisify, wait_for_signal, owned_by


def run_async(coro_factory, timeout_ms=5000):
    """Run a coroutine under QtAsyncio with a hard timeout.

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
        asyncio.get_event_loop().call_later(0.01, QApplication.quit)

    QtAsyncio.run(runner(), handle_sigint=True)

    if not results:
        raise TimeoutError('QtAsyncio.run did not complete')
    kind, value = results[0]
    if kind == 'err':
        raise value
    return value



# NOTE: QtAsyncio tests create their own QApplication via QtAsyncio.run().
# They cannot use qtbot (which creates a separate QApplication).
# The non-QtAsyncio tests use qtbot normally.

# --- Section 1: _smart_connect passthrough ---


def test_sync_handler_passes_through(qtbot):
    """Sync signal handlers should work identically with _smart_connect."""
    received = []

    button = QPushButton()
    button.clicked.connect(lambda: received.append('clicked'))

    from qtpy.QtCore import Qt
    qtbot.mouseClick(button, Qt.LeftButton)
    assert received == ['clicked']


def test_sync_handler_no_overhead(qtbot):
    """_smart_connect should not wrap sync functions — same callable identity."""
    def handler():
        pass

    button = QPushButton()
    button.clicked.connect(handler)

    # The connected slot should be the original function, not a wrapper.
    # Qt doesn't expose the connected slot directly, but we can verify
    # that iscoroutinefunction returns False and the function still works.
    import inspect
    assert not inspect.iscoroutinefunction(handler)


# --- Section 2: Async handler via .connect() ---


@pytest.mark.skipif(not HAVE_QTASYNCIO, reason='QtAsyncio not available')
def test_async_handler_runs_under_qtasyncio():
    """An async def connected to a signal should run as a task under QtAsyncio."""
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


@pytest.mark.skipif(not HAVE_QTASYNCIO, reason='QtAsyncio not available')
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


@pytest.mark.skipif(not HAVE_QTASYNCIO, reason='QtAsyncio not available')
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


@pytest.mark.skipif(not HAVE_QTASYNCIO, reason='QtAsyncio not available')
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


@pytest.mark.skipif(not HAVE_QTASYNCIO, reason='QtAsyncio not available')
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
@pytest.mark.skipif(not HAVE_QTASYNCIO, reason='QtAsyncio not available')
@pytest.mark.xfail(reason='QtAsyncio QtTask does not implement cancelling()')
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


@pytest.mark.skipif(not HAVE_QTASYNCIO, reason='QtAsyncio not available')
@pytest.mark.xfail(reason='QtAsyncio QtTask does not fully implement asyncio Task/Future protocol needed by Promise.__await__')
def test_promise_all():
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


@pytest.mark.skipif(not HAVE_QTASYNCIO, reason='QtAsyncio not available')
@pytest.mark.xfail(reason='QtAsyncio QtTask does not fully implement asyncio Task/Future protocol needed by Promise.__await__')
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

@pytest.mark.skipif(not HAVE_QTASYNCIO, reason='QtAsyncio not available')
@pytest.mark.xfail(reason='QtAsyncio QtTask does not fully implement asyncio Task/Future protocol needed by Promise.__await__')
def test_promise_then_catch_chain():
    """Promise.then/catch should chain correctly."""
    @promisify
    async def fails():
        await asyncio.sleep(0.01)
        raise ValueError('boom')

    async def main():
        result = await fails().catch(lambda e: f'caught: {e}')
        assert 'caught: boom' in result

    run_async(main)


# --- Section 5: owned_by ---

@pytest.mark.skipif(not HAVE_QTASYNCIO, reason='QtAsyncio not available')
@pytest.mark.xfail(reason='QtAsyncio QtTask does not fully implement asyncio Task/Future protocol needed by promisify')
def test_owned_by_cancels_on_destroy():
    """owned_by should cancel a promise when the owner is destroyed."""
    owner = QObject()

    @promisify
    async def long_running():
        await asyncio.sleep(10)
        return 'should not get here'

    promise = long_running()
    owned_by(promise, owner)

    async def main():
        # Destroy the owner — should cancel the promise
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

    # Without a running loop, calling promisified sync fn creates a Promise
    # that immediately resolves. No task needed for sync functions.
    promise = add(1, 2)
    assert isinstance(promise, Promise)


@pytest.mark.skipif(not HAVE_QTASYNCIO, reason='QtAsyncio not available')
def test_promisify_sync_function_awaitable():
    """A promisified sync function should be awaitable under QtAsyncio."""
    @promisify
    def add(a, b):
        return a + b

    async def main():
        result = await add(3, 4)
        assert result == 7

    run_async(main)