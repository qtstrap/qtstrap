---
type: plan
status: accepted
tags: [plan, bugfix, code-review]
keywords: [qtstrap, bugfix, code-review, plan, 2026-07]
summary: Bugfix plan documenting code review findings for qtstrap as of July 2026.
---

# Bugfix Plan: Code Review Findings (2026-07)

Findings from a full review of qtstrap master (HEAD = `25f30b6 Fix logging performance`).
Each item stands alone and can be implemented independently unless a dependency is
noted. Work top to bottom — items are ordered by severity.

Line numbers are as of `25f30b6` and may drift; anchor on the quoted code, not the line.

**General rules for the implementer:**
- qtstrap uses `qtpy` as the binding shim. Import Qt names from `qtstrap` or `qtpy`,
  never directly from PySide6/PyQt.
- Do not change public API signatures unless the item says to.
- A test suite exists under `test/` (pytest + pytest-qt). Run it with
  `QT_QPA_PLATFORM=offscreen uv run pytest test/`. Add a regression test there for
  every item where one is feasible; each item also lists a manual verification step.
- Known-broken at time of writing: `test/test_base_app.py` fails with
  `AppConfigError` — the `7ae3c81 Refactor qtstrap startup sequence` commit made
  `AppInfo` mandatory and the test's `Application` subclass doesn't define one. Fix
  this FIRST (give the test app a minimal `AppInfo`) so the suite is green before
  any other change lands.
- `test/test_layouts.py` has two stub tests (`test_splitter`, `test_scrollarea`)
  that are just `pass` — P0-3 lives exactly in that gap. Fill them as part of P0-3.

---

## P0-1: Portable mode never activates

**Files:** `src/qtstrap/options.py`, `src/qtstrap/__init__.py`, `src/qtstrap/base_application.py`

### Current behavior

`src/qtstrap/__init__.py` decides at **import time** whether to swap the `QSettings`
name for `PortableSettings`:

```python
if OPTIONS.portable:
    from .settings import PortableSettings as QSettings
    QSettings._install()
```

But `OPTIONS.portable` is statically `False` in `options.py`:

```python
class OPTIONS:
    ...
    portable = False
    PORTABLE_SETTINGS_FILE = APPLICATION_PATH / 'settings.ini'
    PORTABLE_FLAG_PATH = APPLICATION_PATH / '.portable'
```

The only code that sets `OPTIONS.portable = True` is `BaseApplication.__init__`
(checks `Path(OPTIONS.PORTABLE_FLAG_PATH).exists()`), which necessarily runs *after*
`import qtstrap` has completed. There is no possible execution order in which the
`if OPTIONS.portable:` branch in `__init__.py` is taken — importing any qtstrap
submodule executes the package `__init__` first. **The branch is dead code, and
portable builds silently write every setting (theme, window geometry, persistent
splitters/widgets) to the registry / native store instead of `settings.ini`.**

### Fix

1. In `options.py`, compute portable-ness at import time, right where the flag path
   is defined:

   ```python
   class OPTIONS:
       APPLICATION_PATH = Path(sys.argv[0]).resolve().parent
       ...
       PORTABLE_FLAG_PATH = APPLICATION_PATH / '.portable'
       portable = PORTABLE_FLAG_PATH.exists()
   ```

2. Leave the alias logic in `__init__.py` as-is — it becomes live once step 1 lands.

3. In `base_application.py`, keep the config-dir override logic but stop re-detecting:

   ```python
   if OPTIONS.portable:
       if OPTIONS.PORTABLE_FLAG_PATH.is_dir():
           OPTIONS.config_dir = OPTIONS.PORTABLE_FLAG_PATH
       else:
           OPTIONS.config_dir = OPTIONS.PORTABLE_FLAG_PATH.parent
   ```

   (Delete the `OPTIONS.portable = True` assignment; preserve the existing
   dir-vs-file behavior exactly — a `.portable` *directory* becomes the config dir
   itself, a `.portable` *file* means "use the application directory".)

### Edge cases

- **Ordering inside `BaseApplication`:** `PortableSettings._install()` sets the ini
  path to `OPTIONS.config_dir / 'settings.ini'`, and it runs at import time — before
  `BaseApplication.__init__` overrides `OPTIONS.config_dir` for the dir-flag case.
  After this fix, `_install()` must be called (again) *after* the config_dir override
  in `BaseApplication.__init__`, or the ini file lands in the wrong directory.
  Simplest: call `PortableSettings._install()` unconditionally at the end of the
  portable branch in `BaseApplication.__init__`.
- **`sys.argv[0]` weirdness:** under frozen apps (PyInstaller) `sys.argv[0]` is the
  exe path — fine. Under embedded interpreters it can be `''`; `Path('').resolve()`
  is the CWD. This is pre-existing behavior; do not try to fix it here.
- **`OPTIONS.theme` reads:** `BaseApplication.__init__` calls `QSettings()` for the
  theme *before* the portable config-dir override happens today. Check the ordering
  after your change: the theme read must happen after `_install()` re-points the ini
  path, or the theme comes from the wrong file.
- **Modules that already imported the name:** anything that did
  `from qtstrap import QSettings` binds whichever object existed at its import time.
  Since qtstrap's own `__init__` performs the swap before any submodule user code
  runs, this is safe — but do not move the swap later in `__init__.py`.

### Verification

Create an empty `.portable` file next to a test app's entry script, run the app,
change the theme, and confirm a `settings.ini` appears next to the app (or inside
the `.portable` dir when it's a directory) and contains the theme key. Confirm
nothing was written to the registry (Windows) / `~/.config` (Linux).

---

## P0-2: `use_async=False` still installs the async handler

**Files:** `src/qtstrap/extras/log_monitor/__init__.py`, `src/qtstrap/extras/log_monitor/async_database_handler.py`

### Current behavior

`async_database_handler.py` ends with a compatibility alias:

```python
DatabaseHandler = AsyncDatabaseHandler
```

and `log_monitor/__init__.py` imports **both names from the async module**:

```python
from .async_database_handler import AsyncDatabaseHandler, DatabaseHandler
...
if use_async:
    logger.addHandler(AsyncDatabaseHandler(database_name))
else:
    logger.addHandler(DatabaseHandler(database_name))
```

So the `use_async=False` branch constructs the async handler under another name. The
real synchronous handler in `log_database_handler.py` is unreachable.

### Fix

Pick ONE of these (recommend A):

- **(A) Remove the pretense.** Delete the `use_async` parameter, delete the
  `DatabaseHandler = AsyncDatabaseHandler` alias line, and delete
  `log_database_handler.py` after confirming nothing imports it
  (`grep -rn "log_database_handler" src/`). Note: `log_widget.py` already imports
  `db_conn_name` from the async module. Keep the alias name `DatabaseHandler`
  exported from `log_monitor/__init__.py` for backwards compat with downstream apps
  (Stagehand imports `DatabaseHandler` in places — check with
  `grep -rn "DatabaseHandler" ../Stagehand/src/`).
- **(B) Make the flag honest.** Import the sync handler from its real module:
  `from .log_database_handler import DatabaseHandler as SyncDatabaseHandler` and use
  it in the `else:` branch. Only do this if there's a real reason to keep the sync
  path alive.

### Edge cases

- Both modules define `db_conn_name = 'logs'`. If both handlers are ever constructed
  in one process they call `QSqlDatabase.addDatabase('QSQLITE', 'logs')` twice — Qt
  logs "duplicate connection name, old connection removed" and yanks the connection
  out from under the first handler. Option A eliminates this class of bug.

### Verification

`grep -n "use_async\|DatabaseHandler" src/qtstrap/extras/log_monitor/*.py` — confirm
one handler class, one connection-name constant, no dead flag.

---

## P0-3: `PersistentCScrollArea` crashes on construction and silently drops children

**File:** `src/qtstrap/widgets/layouts.py` (class near the bottom)

### Current behavior

```python
class PersistentCScrollArea(QScrollArea, ContextLayoutBase):
    def __init__(self, name, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.name = name
        self.scrolled.connect(lambda: QSettings().setValue(self.name, self.saveState()))
```

Four independent problems:

1. `QScrollArea` has **no `scrolled` signal** → `AttributeError` the moment anyone
   calls `ContextLayout.scroll('some_name')`.
2. `QScrollArea` has **no `saveState()`/`restoreState()`** methods → even with a
   real signal this would raise.
3. It does not inherit `CScrollArea`, so it never builds the inner
   widget + `CVBoxLayout` that `CScrollArea.__init__` sets up, and it passes `parent`
   (which may be a `ContextLayoutBase`, i.e. a layout) straight to
   `QScrollArea.__init__` → `TypeError` for non-QWidget parents.
4. It inherits `ContextLayoutBase.add()`, which is a **no-op that returns the item**
   — so in a hypothetical world where construction succeeded, children added inside
   the with-block would be silently discarded.

Nothing in qtstrap or Stagehand constructs this class today, which is why it has
survived — but it is exported public API reachable via `layout.scroll(name=...)`.

### Fix

Rewrite to inherit `CScrollArea` and persist the scrollbar position (there is no
built-in state blob for scroll areas — the scrollbar value *is* the state):

```python
class PersistentCScrollArea(CScrollArea):
    def __init__(self, name: str, parent=None, **kwargs):
        super().__init__(parent, **kwargs)
        self.name = name
        self._restored = False
        self.verticalScrollBar().valueChanged.connect(self._save_state)

    def _save_state(self, value: int) -> None:
        if self._restored:          # don't save while restoring / before restore
            QSettings().setValue(self.name, value)

    def restore_state(self) -> None:
        value = QSettings().value(self.name, None)
        if value is not None:
            self.verticalScrollBar().setValue(int(value))
        self._restored = True

    def __exit__(self, *args):
        # content height is not final at with-block exit; defer restore until
        # the event loop has laid the widget out
        call_later(self.restore_state, 10)
```

### Edge cases

- **QSettings type coercion:** with ini-format settings (portable mode), values come
  back as *strings*. Always `int(value)` before `setValue` on the scrollbar. Wrap in
  `try/except (TypeError, ValueError)` and skip restore on garbage.
- **Restore timing:** at `__exit__` time the scroll area's content widget typically
  has zero height, so `setValue(500)` clamps to 0 and the restore is lost. The
  `call_later` defer handles the common case; a fully robust version restores on the
  first `showEvent` instead. Implement the `showEvent` version if the deferred one
  proves flaky:
  ```python
  def showEvent(self, event):
      super().showEvent(event)
      if not self._restored:
          self.restore_state()
  ```
- **Save storm:** `valueChanged` fires on every scroll pixel. Acceptable for now
  (QSettings writes are cheap-ish and this matches PersistentCSplitter's existing
  behavior); if the debounce utility from the utilities plan lands first, debounce
  the save at ~250ms.
- **The `_restored` guard matters:** without it, programmatic layout during startup
  fires `valueChanged(0)` and overwrites the saved value before restore runs.
- **Key namespace:** the raw `name` is used as a global QSettings key, same as
  PersistentCSplitter. Keep that convention (do not prefix) for compatibility.

### Verification

Fill in the `test_scrollarea` stub in `test/test_layouts.py`: construct via
`layout.scroll('test_scroll')`, add 50 labels, assert they landed in the inner
widget's layout (regression for problem 4 — children silently dropped). Then a
manual pass: scratch app, scroll halfway, restart, confirm the position restores.
Fill the `test_splitter` stub while you're in the file (construct `CSplitter` and
`PersistentCSplitter`, add children, assert `count()`).

---

## P0-4: AsyncDatabaseHandler starts QTimers from worker threads

**File:** `src/qtstrap/extras/log_monitor/async_database_handler.py`

### Current behavior

`emit()` runs on whatever thread called `log.info(...)`. It calls
`_schedule_callback()`, which does `AsyncDatabaseHandler._callback_timer.start(100)`.
Qt hard-requires that `QTimer.start()` be called from the thread that owns the timer
(the main thread here). From any worker thread this prints
`QObject::startTimer: Timers cannot be started from another thread` and the timer
does not start — so **UI refresh notifications for logs emitted from worker threads
are lost** (they only appear when a main-thread log happens to arrive later).

The class declares two signals that are never emitted anywhere:

```python
log_added = Signal()
flush_complete = Signal()
```

These were clearly intended for exactly this purpose.

### Fix

Use the declared signal as the thread crossing. In `__init__` (inside the
`_instance is None` block, after the timers are created):

```python
self.log_added.connect(self._schedule_callback)   # auto connection
```

In `emit()`, replace the direct `self._schedule_callback()` call with:

```python
self.log_added.emit()
```

Qt's AUTO connection delivers the signal directly when emitted from the main thread
and queues it (thread-safe) when emitted from any other thread, so
`_schedule_callback` — and therefore `QTimer.start` — always runs on the handler's
own thread.

### Edge cases

- **The handler must be constructed on the main thread.** Both QTimers and the
  QSqlDatabase connection are created in `__init__` and owned by the constructing
  thread; `_flush_queue` runs off `_flush_timer` in that same thread. Add a guard at
  the top of `__init__`:
  ```python
  app = QApplication.instance()
  if app is not None and QThread.currentThread() is not app.thread():
      raise RuntimeError('AsyncDatabaseHandler must be created on the main thread')
  ```
- **Signal emission before the event loop starts** is fine (queued events are
  processed once `app.exec()` runs); nothing to do.
- **`_pending_callback` race:** it's a plain bool touched from `_schedule_callback`
  (main thread only, after this fix) and reset in `_emit_callbacks` (main thread).
  After the fix all access is main-thread — the race disappears. Do NOT add a lock.
- **QueuedConnection flood:** every `emit()` from a worker thread posts one queued
  event even when a callback is already pending. Under log storms this can flood the
  event queue. Acceptable mitigation: keep a cheap pre-check
  `if not AsyncDatabaseHandler._pending_callback: self.log_added.emit()` in `emit()`.
  This reads `_pending_callback` unlocked from a worker thread — a stale read here
  is harmless (worst case: one extra queued event, or a 100ms-late refresh).

### Verification

In a scratch app, log from a `threading.Thread` in a loop; confirm no
`QObject::startTimer` warnings on the console and that the log monitor UI refreshes
while ONLY worker-thread logs are arriving.

---

## P0-5: Batch INSERT poisoning — one bad record discards up to 500 records

**File:** `src/qtstrap/extras/log_monitor/async_database_handler.py`

### Current behavior

`format_for_insert()` builds a SQL VALUES tuple by f-string interpolation and only
escapes single quotes in `record.msg` and the exception text. Logger `name`, `args`,
`module`, `funcName`, and `threadName` are interpolated raw. A single quote in any of
them (e.g. `log = logging.getLogger("user's-plugin")`, or args containing `'`)
produces invalid SQL. Because `_flush_queue` joins up to 500 records into **one**
`INSERT ... VALUES (...), (...), ...` statement, one malformed record makes the whole
statement fail and **all records in that batch are silently dropped**. The old
synchronous handler lost only the bad record; the batch rewrite made the failure
mode strictly worse.

Additionally `db.exec_()` failures are never checked, so the data loss is invisible.

### Fix

Stop building SQL strings. Queue structured tuples and use a prepared statement with
`execBatch()`:

1. In `emit()`, queue a tuple of the 13 column values (no SQL, no escaping):

   ```python
   values = (
       time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(record.created)),
       record.name,
       record.levelno,
       record.levelname,
       record.getMessage(),          # formatted message — see P1-6
       str(record.args) if record.args else '',
       record.module,
       record.funcName,
       record.lineno,
       exc_text,                     # formatted exception or ''
       record.process,
       str(record.thread),
       record.threadName,
   )
   with AsyncDatabaseHandler._queue_lock:
       AsyncDatabaseHandler._queue.append(values)
   ```

2. In `_flush_queue()`, prepared batch insert inside a transaction:

   ```python
   from qtpy.QtSql import QSqlQuery

   db = QSqlDatabase.database(db_conn_name)
   if not db.isValid() or not db.isOpen():
       return

   query = QSqlQuery(db)
   query.prepare(
       'INSERT INTO log (TimeStamp, Source, LogLevel, LogLevelName, Message, Args,'
       ' Module, FuncName, LineNo, Exception, Process, Thread, ThreadName)'
       ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'
   )
   db.transaction()
   for row in records:
       for value in row:
           query.addBindValue(value)
       if not query.exec_():
           # drop only the bad row, keep the batch
           import logging as _logging
           _logging.getLogger(__name__).warning(
           'log db insert failed: %s', query.lastError().text())
   db.commit()
   ```

   Per-row `exec_()` inside one transaction is nearly as fast as a multi-row VALUES
   and is immune to poisoning. (True `execBatch()` — bind a list per column — is
   also fine; per-row-in-transaction is easier to get right.)

3. Delete `format_for_insert()`, `_insert_in_chunks()` (no longer needed — the
   transaction handles any batch size), and the chunking branch in `_flush_queue`.

4. Fix the PRAGMA execution — the QSQLITE driver executes **only one statement per
   `exec_()` call**, so the current two-PRAGMA string never applies the second one:

   ```python
   db.exec_('PRAGMA journal_mode=WAL')
   db.exec_('PRAGMA synchronous=NORMAL')
   ```

### Edge cases

- **Never log to the root logger from inside the handler** — infinite recursion.
  Log insert failures to `logging.getLogger(__name__)` ONLY if that logger has
  `propagate` semantics that avoid re-entering this handler; the safe simple option
  is `print(..., file=sys.stderr)` or a module-level "failures" counter. Prefer
  stderr.
- **None values:** `record.args` may be None; exc_text may be ''; bind values must
  be str/int/None — QSql binds None as NULL, which the TEXT columns accept. Coerce
  deliberately (as in the sketch) so schema stays consistent with old rows.
- **`record.getMessage()` can raise** if the format string doesn't match args
  (`log.info('%s %s', only_one)`). Wrap the tuple construction in the existing
  `try/except` in `emit()` (it already calls `self.handleError(record)`).
- **Do not hold `_queue_lock` while doing DB work** — the current code copies then
  clears under the lock and inserts outside it; preserve that.
- **Chinese docstring:** `_insert_in_chunks` has "避免巨型 SQL statements" — the
  method is deleted by this fix; make sure the stray text goes with it.

### Verification

Log a message from a logger literally named `it's-a-trap` with args `("don't",)`,
then confirm the row appears in the DB (`sqlite3 log.db 'select * from log order by rowid desc limit 5'`)
alongside 100 normal rows logged in the same 100ms window.

---

## P1-6: Handler mutates the shared LogRecord

**File:** `src/qtstrap/extras/log_monitor/async_database_handler.py`

### Current behavior

```python
record.msg = str(record.msg).replace("'", "''")
```

`LogRecord` instances are shared by every handler on the logger. This line rewrites
the record in place, so any handler that formats *after* this one (console handler,
file handler) prints doubled quotes: `can't open` → `can''t open`. It also stores
`record.msg` — the raw *unformatted* template (`"value: %s"`) — instead of the
rendered message.

### Fix

This is fully subsumed by P0-5 (which stores `record.getMessage()` into a local
tuple and never touches the record). If P0-5 is deferred for any reason, the minimal
standalone fix is: build the escaped string in a local variable, never assign to
`record.msg`.

### Verification

Attach a `StreamHandler` and the DB handler to the same logger; log `can't`;
confirm the console shows `can't` (single quote) and the DB row shows `can't`.

---

## P1-7: A bare `LogMonitorWidget` never polls

**Files:** `src/qtstrap/extras/log_monitor/log_widget.py`, `src/qtstrap/extras/log_monitor/log_table_view.py`

### Current behavior

The perf commit removed `self.scan_timer.start(200)` from `LogTableView.__init__`
(comment: "visibility handler will control it"). The timer is now only started by
`set_visible_state(True)`, which is only called from `showEvent` overrides on
`LogMonitorDockWidget` and `LogMonitorDropdown`. Any app that embeds
`LogMonitorWidget` directly (in a tab, a splitter, its own dialog) gets a table that
**never refreshes** — logs accumulate in the DB but the view stays empty/stale.

### Fix

Move the visibility handling onto `LogMonitorWidget` itself, where every wrapper
inherits it for free:

```python
class LogMonitorWidget(QWidget):
    def showEvent(self, event):
        super().showEvent(event)
        self.set_visible_state(True)

    def hideEvent(self, event):
        super().hideEvent(event)
        self.set_visible_state(False)
```

Then delete the `showEvent`/`hideEvent` overrides from `LogMonitorDockWidget` and
`LogMonitorDropdown` (a child widget receives show/hide events when its ancestors
are shown/hidden, so the wrappers no longer need them). Keep `set_visible_state`
public — the dropdown's manual toggle logic may still call it.

### Edge cases

- **Double toggles are harmless but wasteful:** if you keep the wrapper overrides
  AND add the widget ones, `set_visible_state` runs twice per transition. It's
  idempotent (`QTimer.start` on a running timer just restarts it), but delete the
  wrapper versions for clarity.
- **`hideEvent` also fires on minimize and tab-switch-away** — that's desirable
  (stop polling when not visible), it's the whole point of the perf change.
- **Initial state:** `LogTableView._is_visible` is initialized to `True` but the
  timer isn't running — inconsistent. Initialize `_is_visible = False`; the first
  `showEvent` makes it true. Make sure `attempt_refresh` is called by
  `set_visible_state(True)` (it already is) so a freshly shown view catches up
  immediately.
- **`AsyncDatabaseHandler.set_visible(False)` is class-level:** if an app shows TWO
  log monitors (dock + dropdown), hiding one turns off flush-notifications for both.
  Fix by ref-counting in `set_visible` (increment on True, decrement on False,
  visible iff count > 0) or by tracking visible widgets in a set. Note this in the
  code either way.

### Verification

Scratch app with `LogMonitorWidget` placed directly in a `QVBoxLayout` (no dock);
log messages on a timer; confirm rows appear. Then hide/show the window and confirm
polling stops/resumes (breakpoint or print in `attempt_refresh`).

---

## P1-8: Root logger set to level 1 captures the world

**File:** `src/qtstrap/extras/log_monitor/__init__.py`

### Current behavior

```python
logger = logging.getLogger()
logger.setLevel(1)
```

Level 1 on the **root** logger means every DEBUG record from every third-party
library (urllib3, asyncio, websockets, PIL...) flows into the SQLite handler. This
is very likely the original source of the "logging performance" problem the async
handler was built to mitigate — the volume, not the per-insert cost.

### Fix

Add a `level` parameter, defaulting to something sane:

```python
def install(database_name=None, install_excepthook=True, level=logging.DEBUG):
    ...
    logger.setLevel(level)
```

`logging.DEBUG` (10) as the default keeps app-authored debug logs while cutting the
level-1..9 noise; document that apps drowning in third-party debug spam should pass
`level=logging.INFO` and/or raise levels on specific noisy loggers:

```python
logging.getLogger('urllib3').setLevel(logging.WARNING)
```

### Edge cases

- **Backwards compat:** any app relying on sub-DEBUG custom levels (levels 1–9)
  would lose records. Default to `logging.DEBUG`, not `INFO`, precisely to keep this
  change low-risk; the parameter gives apps the escape hatch in both directions.
- Also consider `handler.setLevel(...)` vs `logger.setLevel(...)`: setting only the
  handler level still pays record-creation cost for suppressed records. Set the
  logger level (as now) — it short-circuits earlier.

### Verification

Install with defaults, import `urllib3` and make a request; confirm the DB doesn't
fill with urllib3 connection-pool debug rows (it will at level 1).

---

## P1-9: Excepthook logs the wrong source location

**File:** `src/qtstrap/extras/log_monitor/__init__.py`

### Current behavior

```python
def handle_exception(exc_type, exc_value, exc_traceback):
    module = exc_traceback.tb_frame.f_code.co_filename
    lineno = exc_traceback.tb_lineno
    funcName = exc_traceback.tb_frame.f_code.co_name
```

`exc_traceback` is the **outermost** frame — usually `main.py:1, in <module>` — not
the frame that raised. Every logged exception points at the program entry point.

### Fix

Walk to the innermost frame first:

```python
def handle_exception(exc_type, exc_value, exc_traceback):
    tb = exc_traceback
    if tb is not None:
        while tb.tb_next is not None:
            tb = tb.tb_next
        module = tb.tb_frame.f_code.co_filename
        lineno = tb.tb_lineno
        funcName = tb.tb_frame.f_code.co_name
        msg = f'[{module}:{lineno}, in {funcName}] {exc_type.__name__} {exc_value}'
    else:
        msg = f'{exc_type.__name__} {exc_value}'

    exception_logger.error(msg, exc_info=(exc_type, exc_value, exc_traceback))
    _excepthook(exc_type, exc_value, exc_traceback)
```

### Edge cases

- `exc_traceback` can be `None` (e.g. exceptions raised in C extensions or
  re-raised synthetically) — handle it, as above.
- Do **not** swallow `KeyboardInterrupt` differently here — the chained
  `_excepthook` call already preserves default behavior. Leave the chaining exactly
  as-is.
- The full traceback is still logged via `exc_info=`, so nothing is lost — this fix
  only corrects the one-line summary.

### Verification

Raise an exception three calls deep in a scratch app; confirm the logged summary
names the innermost file/line/function.

---

## P2-10: `@singleton` replaces the class with a function

**File:** `src/qtstrap/utils/singleton.py`

### Current behavior

```python
def singleton(class_):
    def getinstance(*args, **kwargs):
        if class_ not in instances:
            instances[class_] = class_(*args, **kwargs)
        return instances[class_]
    return getinstance
```

After decoration, the name `Test` is a *function*. Consequences:
`isinstance(x, Test)` raises `TypeError`; `Test.some_class_attr` fails
(`AttributeError` on a function); subclassing is impossible; type checkers and IDEs
lose the class entirely.

### Fix

Preserve the class; intercept construction via `__new__` + a re-init guard:

```python
instances = {}


def singleton(class_):
    """
    Class decorator that only allows one instance to be created.
    The decorated name remains a real class: isinstance, class attributes,
    and subclass definitions all keep working.
    """
    original_new = class_.__new__
    original_init = class_.__init__

    def __new__(cls, *args, **kwargs):
        if cls not in instances:
            if original_new is object.__new__:
                instances[cls] = original_new(cls)
            else:
                instances[cls] = original_new(cls, *args, **kwargs)
        return instances[cls]

    def __init__(self, *args, **kwargs):
        if getattr(self, '_singleton_initialized', False):
            return
        self._singleton_initialized = True
        original_init(self, *args, **kwargs)

    class_.__new__ = __new__
    class_.__init__ = __init__
    return class_
```

### Edge cases

- **The re-init guard is mandatory.** Python calls `__init__` every time
  `Test()` is evaluated, even when `__new__` returns an existing instance. Without
  the guard, `Test()` a second time re-runs `__init__` on the shared instance —
  for QObject singletons that would re-create child widgets, reconnect signals, etc.
- **`object.__new__` signature:** plain `object.__new__` rejects extra args when
  `__init__` is overridden in some interpreter paths — hence the branch in the
  sketch. Qt classes (Shiboken/SIP) have their own `__new__` that tolerates args.
- **Keyed by `cls`, not `class_`:** if someone subclasses a singleton class, each
  subclass gets its own instance (keyed on the actual class). This is the least
  surprising behavior; the old code couldn't be subclassed at all.
- **Do NOT use a metaclass** — Qt classes already have a Shiboken/SIP metaclass and
  mixing metaclasses raises `metaclass conflict` errors.
- **Thread safety:** construction is not locked. All current uses construct on the
  main thread; add a `threading.Lock` around the `if cls not in instances` check
  only if a real cross-thread constructor shows up. Document this in the docstring.
- **Downstream contract check:** Stagehand calls `Sandbox()`, `App()` etc. — the
  `Test() is Test()` contract is preserved. Run Stagehand after upgrading to
  confirm (it exercises `@singleton` on QObject subclasses heavily).
- **Keep the module-level `instances` dict public** — the future `qtstrap.testing`
  module (see utilities plan) needs to clear it between tests.

### Verification

Extend the existing `test/utils/test_singleton.py` (it already asserts
`Test() is Test()`) with isinstance and init-once checks:

```python
def test_singleton():
    @singleton
    class T:
        def __init__(self):
            self.count = getattr(self, 'count', 0) + 1

    a, b = T(), T()
    assert a is b
    assert isinstance(a, T)
    assert a.count == 1        # __init__ ran once
```

---

## P2-11: Assorted small fixes

Each of these is a few lines. File: `src/qtstrap/widgets/layouts.py` unless noted.

### (a) `CSplitter` silently ignores QLayout parents

```python
elif isinstance(parent, QLayout):
    # TODO: implement this
    pass
```

The splitter is constructed but never added — it leaks, invisible. Until it's
implemented, fail loudly:

```python
elif isinstance(parent, QLayout):
    raise NotImplementedError('CSplitter cannot be parented to a raw QLayout yet')
```

### (b) `CFormLayout.add()` explodes strings

`str` is a `Sequence`, so `add('hello')` (b=None) reaches
`self._layout.addRow(*a)` → `addRow('h','e','l','l','o')` → TypeError with a
baffling message. Guard strings before the Sequence branch:

```python
if isinstance(a, str):
    raise TypeError('CFormLayout.add() needs a (label, widget) pair, got a bare string')
```

### (c) `ContextLayout.__getattr__` recursion trap

If any missing attribute is accessed before `self._stack` is assigned (last line of
`__init__`), `__getattr__('_stack')` → `_layout` property → `self._stack` →
`__getattr__('_stack')` → `RecursionError`. Two-line guard at the top of
`__getattr__`:

```python
def __getattr__(self, name: str):
    if name in ('_stack', 'next_layout'):
        raise AttributeError(name)
    return getattr(self._layout, name)
```

Alternatively (also do this — it's free): assign `self._stack = []` and
`self.next_layout = None` as the FIRST statements of `ContextLayout.__init__`,
before any `super().__init__` calls.

### (d) `PersistentCSplitter` save storm

`splitterMoved` fires per-pixel during a drag; each firing writes QSettings. Either
debounce with a single-shot QTimer (~250ms) or save once in `__exit__` and on
`App().aboutToQuit`. If the debounce utility from the utilities plan exists, use it.
Edge case: whatever you choose, ensure a save happens if the app closes mid-drag
(aboutToQuit hook covers it).

### (e) Delete `log_monitor_diagnostic.py` from the repo root

A 522-line diagnostic script committed with the perf work. `git rm` it, or move to
`tools/` if it's still useful for benchmarking the P0-5 rewrite (it may be! consider
running it before/after).

### (f) Version-compare crash bait in downstream apps (informational)

Not a qtstrap file, but recorded here because it was found in the same review:
Stagehand's `app_updater.py` compares versions with `float(tag_name)` — breaks on
`1.10` and any `x.y.z` tag. The updater is slated to move into qtstrap (see
utilities plan §4) — fix the comparison during the move, don't fix it twice.

---

## Extras addendum (2026-07-10): command_palette, devtools, style, settings_model

Second review pass covering the extras not read in the first pass. Items P1-12 and
P1-13 were **empirically confirmed** (reproduced in a live interpreter), not just
read off the source.

### P1-12: Command palette crashes on regex metacharacters — CONFIRMED

**File:** `src/qtstrap/extras/command_palette/command_palette.py`, `PopupDelegate.paint()`

The user's typed filter text is passed to `re.split` as a **raw regex pattern**:

```python
parts = re.split(prefix, value, flags=re.IGNORECASE)
```

Typing `(`, `[`, `*`, `+`, `?`, or `\` into the palette raises `re.error`
(confirmed: `re.split('(', ...)` → `missing ), unterminated subpattern`) — inside a
**paint event**, once per visible row per frame, which floods stderr and breaks
rendering for as long as the character is in the box.

**Fix:** escape at the split site:

```python
parts = re.split(re.escape(prefix), value, flags=re.IGNORECASE)
```

The `prefix.lower() in value.lower()` guard above it and the highlight-slicing
logic below it operate on literal text and are unaffected.

**Edge cases:** the same raw `prefix` is used in `CommandModel.sort_commands` via
`in` (substring — safe, leave it). Test with a prefix that is ALSO a valid regex
(`.`) — before the fix it silently matches everything in the split (wrong
highlighting); after the fix it matches only literal dots.

**Verification:** add a unit test that constructs `PopupDelegate`, sets prefix
`'('`, and paints into a `QPixmap`-backed `QPainter` over a one-item model. Manual:
open palette, type `(`.

### P1-13: `CommandRegistry` never calls `QObject.__init__` — CONFIRMED

**File:** same file, top:

```python
class CommandRegistry(QObject):
    def __init__(self) -> None:
        self.registry = {}       # no super().__init__()
        self.commands = []
```

Confirmed behavior: **any** Qt-side use of the module-global `registry` raises
`RuntimeError: '__init__' method of object's base class (CommandRegistry) not
called`. It hasn't exploded yet only because the current code never touches a Qt
method on it. The first person to add a signal to the registry (e.g.
`commands_changed = Signal()` — the obvious next feature) gets a crash at emit.

**Fix:** add `super().__init__()` as the first line. One line, zero risk.

### P2-14: Command registry lifecycle and model desync

**File:** same file.

Three related defects, fix together:

1. **Commands are never unregistered.** `Command.__init__` registers into a
   module-global registry; nothing removes entries when the owning widget dies.
   Dead commands stay listed in the palette forever, and executing one emits
   `triggered` on a deleted QAction → `RuntimeError`. Fix: in `Command.__init__`,
   `self.destroyed.connect(lambda _=None, text=self.text(): registry.unregister(text))`
   and implement `CommandRegistry.unregister(name)` (pop from dict, rebuild list).
   Edge case: capture the text at connect time — inside a `destroyed` handler the
   Python wrapper is already half-dead and `self.text()` may raise.
2. **`rowCount` and `data` read different lists.** `rowCount` returns
   `len(registry.commands)` but `data()` indexes `self.sorted_commands`, which is
   only rebuilt by `update_prefix()`. Register (or unregister) a command while the
   palette is open and the lengths diverge → `IndexError` in `data()`. Fix:
   `rowCount` should return `len(self.sorted_commands)`, and the model should call
   `beginResetModel()/endResetModel()` in `sort_commands`.
3. **`sorted_commands = []` is a mutable class attribute** — make it an instance
   attribute in `__init__` (add one; the model currently has none).

Also worth doing while in the file (cosmetic, no separate item): `usage_count` is
incremented and never read — either sort by it in `sort_commands` (frecency, the
obvious intent) or delete it; `PopupDelegate.get_colors` hardcodes selected-text
white and highlight cyan — the March color fix made the *backgrounds* theme-aware
but white-on-`#b0c4d1` (light theme selection) is poor contrast; derive the
selected pen from `palette.color(QPalette.HighlightedText)` or pick per-lightness
like the background. And `center_on_parent()` dereferences `self.parent()` — the
singleton is constructed with whatever parent the *first* caller passed; if that
was `None`, opening the palette crashes. Guard: fall back to
`QApplication.activeWindow()` or screen center.

### P2-15: Scene tree devtool — rescan shows an empty tree, `inverse` leaks

**File:** `src/qtstrap/extras/devtools/scene_tree.py`

`TreeNode.inverse` is a **class-level** dict mapping QObject → node. The cleanup
path (`obj_destroyed`) is written but its `destroyed.connect` line is commented
out, so entries are never removed. Consequences:

1. `SceneTree.scan()` calls `self.clear()` (destroys the items) but `inverse`
   keeps every previously-seen object; `TreeNode.scan()` skips children found in
   `inverse` → a **second scan produces a nearly empty tree** (root only).
2. Dead QObjects accumulate in the dict for the app's lifetime.

**Fix:** clear the dict at the top of `SceneTree.scan()`
(`TreeNode.inverse.clear()`), and re-enable the destroyed hookup — but see the
edge case: `self.obj.destroyed.connect(self.obj_destroyed)` passes the half-dead
object; look it up by identity in `inverse` and guard all Qt calls on the item
with `isValid()` (the code already imports `isValid`/`delete` from
`qtpy.shiboken`). Note `qtpy.shiboken` only exists under PySide bindings — under
PyQt it's `sip.isdeleted` with inverted semantics; if the PyQt5/6 tox envs are kept,
this import is already a latent break worth a `qtpy.API_NAME` guard.

Same file, small: `contextMenuEvent` uses `self.itemAt(...)` without a None check —
right-clicking empty space crashes (`item.obj` on None). Early-return on None. The
'Open REPL' and 'Edit Style' context-menu actions are unconnected no-ops — delete
them or wire them to the existing `repl.py` / `style_editor.py` widgets.

### P2-16: Style and settings_model small items

- **`extras/style/themes.py`:** see [../theming-guide.md](../theming-guide.md)
  §4.2 for the full treatment — the minimal fixes are: use `fusion` for BOTH
  themes (not `windowsvista`, which ignores the palette and doesn't exist off
  Windows), apply style BEFORE palette (`setStyle` can reset the palette), and
  add the missing `polish` call after `unpolish`. If implementing the theming
  guide's registry anyway, skip the minimal patch and do §4.1–4.2 directly.
- **`extras/settings_model/settings_model.py`:** `model_state` is keyed by
  `cls.__name__` — two SettingsModel subclasses with the same class name in
  different modules share (and corrupt) each other's load-guard flag. Key by the
  class object itself (`model_state[cls]`). Also `field.default` is
  `PydanticUndefined` for required fields — that sentinel gets passed to
  `QSettings().value()` as the fallback and then into validation; decide the
  behavior (skip loading required-but-unsaved fields, or raise a clear error).

### P1-17: `Adapter.kill()` is a silent no-op — CONFIRMED, root cause identified

**File:** `src/qtstrap/utils/adapter.py`

Running the file's own `__main__` demo shows the mirror adapter still receives
signals after `kill()` (output: original, copy, original, **copy**). The test
file (`test/utils/test_signal_adapter.py`) has the kill() assertions commented
out — this was fought before and parked.

**Root cause (empirically verified):** the adapter connects to
`getattr(other, name).connect(getattr(self, name).emit)`. A `SignalInstance`'s
`.emit` is a **fresh bound-method object on every attribute access**, so no later
`disconnect(...)` call can ever match it — this single fact explains the
docstring's "I've never gotten .disconnect() to work reliably." The current
`kill()` additionally uses old-style `SIGNAL(name)` without a signature, which
also never matches.

**Fix (one word + simplification), all three verified working under PySide6:**

1. Connect **signal-to-signal** — drop `.emit`:
   ```python
   getattr(other, name).connect(getattr(self, name))
   ```
2. `kill()` then works two ways — pick either:
   - `getattr(self._other, name).disconnect(getattr(self, name))` — signals
     match by identity (verified), or
   - simply `self.deleteLater()` — signal-to-signal connections auto-drop when
     the receiver QObject is destroyed (verified). This is the truly nuclear
     version and makes `kill()` five lines shorter.
3. Restore the commented-out assertions in `test_signal_adapter.py` — they
   should pass as written once the fix lands.

**Edge cases:** signal-to-signal requires matching (or contravariant) signatures
— same-named signals on the same class always match, so the Adapter pattern is
safe. If `kill()` uses `deleteLater()`, document that the adapter object is dead
afterward (accessing it raises) — that's the semantic the docstring already
promises. Alternative belt-and-braces: store the `QMetaObject.Connection`
objects returned by `connect()` and `QObject.disconnect(conn)` each — also
verified working — but signal-to-signal is simpler and fixes auto-cleanup too.

**Downstream note:** codex's `SigBundle`/`SlotBundle` are the draft this class
supersedes (see codex lode plans/v2-directions.md) — fixing Adapter here
unblocks migrating codex's subscription internals onto it.

### Verified non-issues (checked, do not "fix")

- `CodeEditor.update_tab_width` calling `setTabStopWidth` on Qt6: PySide6 still
  provides it as a compat alias — constructs and runs fine (confirmed empirically).
- `SettingsModel`'s nested `class Config` under pydantic 2.9: works (confirmed).
  Pydantic may eventually drop tolerance for nested `Config` on models using
  `model_config`; migrating `prefix` to `model_config` extra data is a nice-to-have,
  not a bug.

---

## Suggested implementation order

| Order | Item | Why first |
|-------|------|-----------|
| 1 | P0-1 portable | One-line core fix, everything else benefits from testable settings |
| 2 | P2-10 singleton | Unit-testable in isolation; unblocks `qtstrap.testing` later |
| 3 | P0-5 + P1-6 batch insert | Biggest data-loss risk; P1-6 falls out for free |
| 4 | P0-4 timer threading | Same file as #3, do while context is loaded |
| 5 | P1-7 + P1-8 log widget/level | Same subsystem, completes the log-monitor pass |
| 6 | P0-2 use_async | Trivial once the handler file has settled |
| 7 | P0-3 scroll area | Independent, needs a scratch app to verify |
| 8 | P1-9 + P2-11 | Small fixes, any time |

After the log-monitor items (3–6), re-run `log_monitor_diagnostic.py` (before
deleting it per P2-11e) and compare against the numbers in its own output from the
original perf investigation.
