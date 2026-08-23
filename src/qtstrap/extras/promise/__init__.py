"""qtstrap promise layer — re-exports promisio plus Qt-specific helpers.

The core promise implementation is vendored verbatim from promisio
(https://github.com/miguelgrinberg/promisio) in `_promisio.py`.
Do not modify that file — copy upstream fixes in directly.

This module adds Qt-specific helpers:
- wait_for_signal: await a Qt signal from inside an async island
- owned_by: cancel a promise when its consumer QObject is destroyed
"""

from ._promisio import Promise, promisify, AggregateError, TaskPromise, run

from qtstrap import QObject, Signal
import asyncio


def wait_for_signal(signal, *, timeout: float | None = None, owner: QObject = None):
    """Return an awaitable that resolves with the signal's arguments.

    Single-shot: disconnects itself after the first emission.

    Args:
        signal: the Qt signal to wait for.
        timeout: optional timeout in seconds.
        owner: if provided, the future is cancelled if this QObject is
            destroyed before the signal fires.

    Returns:
        An awaitable that resolves with the signal's first argument (or
        None for zero-arg signals, or a tuple for multi-arg signals).
    """
    loop = asyncio.get_event_loop()
    future = loop.create_future()

    def handler(*args):
        signal.disconnect(handler)
        if not future.done():
            future.set_result(args[0] if len(args) == 1 else args if args else None)

    signal.connect(handler)

    if owner is not None:
        owner.destroyed.connect(lambda *_: future.cancel() if not future.done() else None)

    if timeout is not None:
        return asyncio.wait_for(future, timeout)
    return future


def owned_by(promise, owner: QObject):
    """Cancel the promise when its consumer is destroyed.

    Restores Qt's auto-disconnect property for promise callbacks, which
    hold self past widget destruction.

    Args:
        promise: the Promise to cancel.
        owner: the QObject whose destruction cancels the promise.

    Returns:
        The promise (for chaining).
    """
    owner.destroyed.connect(lambda *_: promise.cancel())
    return promise


__all__ = [
    'Promise',
    'promisify',
    'AggregateError',
    'TaskPromise',
    'run',
    'wait_for_signal',
    'owned_by',
]