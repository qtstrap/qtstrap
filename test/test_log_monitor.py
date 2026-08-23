"""Tests for AsyncDatabaseHandler — thread safety and basic logging."""
import logging
import os
import sqlite3
import tempfile
import threading

import pytest
from qtpy.QtCore import QThread
from qtpy.QtWidgets import QApplication

from qtstrap.extras.log_monitor.async_database_handler import AsyncDatabaseHandler


@pytest.fixture
def db_path():
    fd, path = tempfile.mkstemp(suffix='.db')
    os.close(fd)
    yield path
    for p in [path, path + '-wal', path + '-shm']:
        try:
            os.unlink(p)
        except FileNotFoundError:
            pass


@pytest.fixture
def handler(qtbot, db_path):
    """Create an AsyncDatabaseHandler on the main thread."""
    h = AsyncDatabaseHandler(db_path)
    yield h
    for name in list(logging.Logger.manager.loggerDict.keys()):
        logger = logging.getLogger(name)
        if h in logger.handlers:
            logger.removeHandler(h)
    root = logging.getLogger()
    if h in root.handlers:
        root.removeHandler(h)
    h.close()
    AsyncDatabaseHandler._instance = None
    AsyncDatabaseHandler._queue = None
    AsyncDatabaseHandler._queue_lock = None
    AsyncDatabaseHandler._flush_timer = None
    AsyncDatabaseHandler._callback_timer = None
    AsyncDatabaseHandler._pending_callback = False
    AsyncDatabaseHandler.callbacks = []
    AsyncDatabaseHandler._is_visible = True


def test_handler_constructs_on_main_thread(handler):
    """Handler should construct successfully on the main thread."""
    assert AsyncDatabaseHandler._instance is handler
    assert AsyncDatabaseHandler._flush_timer is not None
    assert AsyncDatabaseHandler._callback_timer is not None


def test_handler_rejects_worker_thread_construction(qtbot, db_path):
    """Handler should raise RuntimeError if constructed off the main thread."""
    errors = []

    def construct_off_main():
        try:
            AsyncDatabaseHandler(db_path)
        except RuntimeError as e:
            errors.append(str(e))

    t = threading.Thread(target=construct_off_main)
    t.start()
    t.join()

    assert len(errors) == 1
    assert 'main thread' in errors[0].lower()


def test_log_from_worker_thread_triggers_callback(handler, qtbot):
    """Logging from a worker thread should trigger the UI callback."""
    logger = logging.getLogger('test_worker')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    called = threading.Event()

    def callback():
        called.set()

    AsyncDatabaseHandler.callbacks = [callback]

    def log_from_thread():
        logger.info('hello from worker')

    t = threading.Thread(target=log_from_thread)
    t.start()
    t.join()

    qtbot.waitUntil(called.is_set, timeout=2000)
    assert called.is_set()


def test_log_from_main_thread_triggers_callback(handler, qtbot):
    """Logging from the main thread should also trigger the callback."""
    logger = logging.getLogger('test_main')
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)

    called = threading.Event()

    def callback():
        called.set()

    AsyncDatabaseHandler.callbacks = [callback]

    logger.info('hello from main')

    qtbot.waitUntil(called.is_set, timeout=2000)
    assert called.is_set()


def test_sql_injection_does_not_poison_batch(handler, qtbot, db_path):
    """A logger name with a single quote should not corrupt the batch."""
    root = logging.getLogger()
    root.addHandler(handler)
    root.setLevel(logging.DEBUG)

    # Log 100 normal messages + 1 with a quote in the logger name
    for i in range(100):
        root.info(f'message {i}')
    logging.getLogger("it's-a-trap").info("don't break the batch")

    # Force flush
    AsyncDatabaseHandler.force_flush()

    # Verify all rows made it to the DB
    conn = sqlite3.connect(db_path)
    cursor = conn.execute('SELECT COUNT(*) FROM log')
    count = cursor.fetchone()[0]
    conn.close()

    # All 101 messages should be in the DB
    assert count >= 101