# Plan: New Utilities for qtstrap

> **See also:** [../async-guide.md](../async-guide.md) — the async interop design
> (promise layer, merged loop, `extras/promise`) and the plan for packaging these
> utilities onto `BaseApplication` as declarative flags with a `run()` entry point.
> Items §1, §4, §5, §6 below are consumed by that packaging design; implement the
> utilities standalone first, flags second.

Nine additions, ranked by evidence of need across qtstrap's downstream apps
(Stagehand, DeviceManager, codex-engine consumers, etc.). The unifying observation: qtstrap has
strong answers for **layout** and **persistence**, and nothing for **concurrency** —
and concurrency is where the real bugs in downstream apps have been (e.g. Stagehand
executing QuickJS tasks and touching UI from a pynput listener thread).

Items 1–3 are the concurrency kit and should land first, in order — item 2 depends
on item 1, and several later items (and bugfix-plan items) want item 3's debounce.

**General rules for the implementer:**
- Import Qt through `qtpy` (qtstrap's binding shim) — never PySide6/PyQt directly.
- New utils live in `src/qtstrap/utils/<name>.py` and must be re-exported from
  `src/qtstrap/utils/__init__.py` (see how `call_later` is exported).
- New widgets live in `src/qtstrap/widgets/`, larger opt-in subsystems in
  `src/qtstrap/extras/<name>/`.
- Zero new runtime dependencies for items 1–8. Item 9 adds `pytest` (dev only).
- Every public callable gets a docstring with a usage example — qtstrap's existing
  style (see `utils/singleton.py`).

---

## 1. Main-thread marshaling — `utils/thread_marshal.py`

### Motivation

Qt requires all widget access and most QObject interaction to happen on the main
thread. Every downstream app hits this: serial-port callbacks, pynput listener
callbacks, websocket handlers, `logging` handlers. Qt's native answers
(`QMetaObject.invokeMethod`, hand-wired queued signals) are verbose and easy to get
wrong. Stagehand currently executes JS tasks *inside a pynput keyboard-hook
callback* — a bug this utility makes trivially avoidable.

### API

```python
from qtstrap import run_on_main, on_main_thread, assert_main_thread, is_main_thread

run_on_main(lambda: label.setText('hi'))          # fire and forget
run_on_main(fn, force_queue=True)                  # queue even if already on main
result = run_on_main_sync(fn, timeout_ms=5000)     # block until fn returns

@on_main_thread
def update_ui(self, text): ...                     # decorated fn always runs on main

assert_main_thread()                               # raises off-main (debug guard)
is_main_thread()                                   # bool
```

### Implementation

A module-private dispatcher QObject that lives on the main thread, with a signal
carrying a callable. Cross-thread `emit` on a queued connection is one of the few
officially thread-safe operations in Qt — that's the entire trick.

```python
from qtpy.QtCore import QObject, Signal, QThread, QCoreApplication


class _MainThreadDispatcher(QObject):
    dispatch = Signal(object)   # carries a zero-arg callable

    def __init__(self):
        super().__init__()
        self.dispatch.connect(self._run)   # AUTO: queued when emitted off-main

    def _run(self, fn):
        try:
            fn()
        except Exception:
            import traceback
            traceback.print_exc()   # never let a marshaled fn kill the event loop


_dispatcher = None


def _get_dispatcher():
    global _dispatcher
    app = QCoreApplication.instance()
    if app is None:
        raise RuntimeError('run_on_main requires a QApplication to exist')
    if _dispatcher is None:
        _dispatcher = _MainThreadDispatcher()
        _dispatcher.moveToThread(app.thread())   # in case first call is off-main
    return _dispatcher


def is_main_thread() -> bool:
    app = QCoreApplication.instance()
    return app is not None and QThread.currentThread() is app.thread()


def run_on_main(fn, *args, force_queue=False, **kwargs):
    """Run fn(*args, **kwargs) on the main thread. Fire-and-forget."""
    from functools import partial
    call = partial(fn, *args, **kwargs)
    if is_main_thread() and not force_queue:
        call()
        return
    _get_dispatcher().dispatch.emit(call)
```

`run_on_main_sync` wraps the same mechanism with a `threading.Event` and a result
slot; `on_main_thread` is a decorator that wraps the function in `run_on_main`.

### Edge cases — read carefully, this is the subtle one

- **Dispatcher creation off-main:** if the first `run_on_main` call happens on a
  worker thread, the dispatcher QObject would be created there and own that thread's
  event loop (which doesn't run). The `moveToThread(app.thread())` call handles this
  — do not remove it. Also guard dispatcher creation with a `threading.Lock` (two
  worker threads racing to create it).
- **`run_on_main_sync` called FROM the main thread must execute inline.** If it
  queues and blocks, the event loop can never process the queued call — instant
  deadlock. Check `is_main_thread()` first and just call the function.
- **`run_on_main_sync` timeout:** always take a `timeout_ms` (default a few
  seconds, `None` = forever) and raise `TimeoutError` on expiry. Without it, a
  deadlock elsewhere silently hangs the worker forever.
- **Exception propagation for sync:** capture the exception in the main-thread slot
  and re-raise it in the *calling* thread after the event fires (store
  `(result, exc)` on the wait object).
- **Shutdown:** queued calls arriving after `QApplication` teardown either get
  dropped (fine) or fire against dead widgets (crash — but that's the caller's bug:
  the callable captured a widget reference). Connect `app.aboutToQuit` to set a
  module flag; `run_on_main` becomes a no-op (with a stderr warning) once quitting.
- **Inline-vs-queued semantics:** executing inline when already on main is the
  default because it's what callers expect from a function call, but it changes
  re-entrancy (fn runs *now*, mid-caller, not after the current event). That's why
  `force_queue=True` exists — document both behaviors in the docstring with one
  sentence each.
- **`Signal(object)` payloads:** qtpy/PySide6 `Signal(object)` carries arbitrary
  Python objects (including partials) across threads safely. Do NOT try
  `Signal(callable)` — not a Qt metatype.
- **`assert_main_thread` before the app exists** should be a no-op (import-time
  code paths), not a crash.

### Testing

`pytest-qt` provides a `qtbot` and a running app. Spawn a `threading.Thread` that
calls `run_on_main` to append to a list; `qtbot.waitUntil(lambda: list_populated)`.
Test the sync deadlock guard by calling `run_on_main_sync` from the main thread.

---

## 2. Background worker — `utils/run_in_thread.py`

Depends on item 1.

### Motivation

The QThreadPool + QRunnable + result-signal dance is retyped in every app that does
network/serial/disk work. Provide the 90% case in one call.

### API

```python
task = run_in_thread(
    fetch_data, args=(url,),
    on_result=self.populate,      # called on MAIN thread with return value
    on_error=self.show_error,     # called on MAIN thread with the exception
    on_finished=self.hide_spinner # called on MAIN thread, always, after result/error
)
```

### Implementation

A `QRunnable` subclass that runs the fn, captures result or exception, then
delivers callbacks via `run_on_main` (item 1). Submit to
`QThreadPool.globalInstance()`.

```python
class _Task(QRunnable):
    def __init__(self, fn, args, kwargs, on_result, on_error, on_finished):
        super().__init__()
        ...

    def run(self):
        try:
            result = self.fn(*self.args, **self.kwargs)
        except Exception as e:
            e.traceback_text = traceback.format_exc()   # attach for the handler
            if self.on_error:
                run_on_main(self.on_error, e)
        else:
            if self.on_result:
                run_on_main(self.on_result, result)
        finally:
            if self.on_finished:
                run_on_main(self.on_finished)
```

### Edge cases

- **No callback = swallowed exception.** If `on_error` is None, print the traceback
  to stderr — never silently eat it.
- **GC:** `QRunnable` with `setAutoDelete(True)` (default) is deleted by the pool
  after `run()`; keep the Python-side references (fn, callbacks) on the runnable
  itself so nothing is collected early. Return the task object so callers *can*
  hold it, but don't require it.
- **Cancellation is out of scope** — provide `task.cancelled` as a cooperative
  flag the fn may poll (`if task.cancelled: return`), nothing stronger. Document
  that already-running work cannot be killed.
- **Shutdown:** workers running at quit can outlive the app and crash in their
  callbacks. The `run_on_main` quit-flag (item 1) absorbs the callback side. For
  the worker side, optionally `QThreadPool.globalInstance().waitForDone(3000)` in
  an `aboutToQuit` hook — make it opt-in (`qtstrap.utils.run_in_thread.install_shutdown_wait()`),
  since blocking quit for 3s is a policy decision.
- **Don't touch Qt objects in the worker fn** — can't be enforced, but say it
  loudly in the docstring, and mention `assert_main_thread()` as the tripwire.
- **QThread vs QThreadPool:** stick to the pool. Long-lived dedicated-thread
  workers (serial port readers) are a different pattern; out of scope here.

### Testing

pytest-qt: run a fn that sleeps 50ms and returns 42; assert `on_result` got 42 on
the main thread (`is_main_thread()` inside the callback). Run a fn that raises;
assert `on_error` received the exception and `on_finished` still fired.

---

## 3. `@debounce` / `@throttle` — `utils/rate_limit.py`

### Motivation

Hand-rolled at least three times in qtstrap alone: the AsyncDatabaseHandler
callback debounce, the LogTableView poll timer, and `PersistentCSplitter` needs one
(it currently writes QSettings on every pixel of a splitter drag). Natural sibling
to `call_later`.

### API

```python
@debounce(250)                 # ms; trailing-edge: fires 250ms after the LAST call
def save_state(self): ...

@throttle(100)                 # leading-edge: fires at most once per 100ms
def on_scroll(self, value): ...

search_box.textChanged.connect(debounce(300)(self.run_search))   # inline use
```

### Implementation

Decorator holding a single-shot `QTimer` per *bound instance* (not per class!),
last-call-wins for arguments:

```python
import weakref
from functools import wraps
from qtpy.QtCore import QTimer


def debounce(msec: int):
    def decorator(fn):
        timers = weakref.WeakKeyDictionary()    # instance -> (QTimer, last_args)
        # a sentinel key for plain functions (no self)
        ...
        @wraps(fn)
        def wrapper(*args, **kwargs):
            key = args[0] if args and _looks_like_method(fn, args) else _module_sentinel
            entry = timers.get(key)
            if entry is None:
                timer = QTimer(singleShot=True)
                entry = {'timer': timer, 'pending': None}
                timer.timeout.connect(lambda: _fire(entry))
                timers[key] = entry
            entry['pending'] = (args, kwargs)
            entry['timer'].start(msec)
        return wrapper
    return decorator
```

(Implementation detail: distinguishing bound methods from plain functions is
awkward at decoration time. The pragmatic approach: key the WeakKeyDictionary on
`args[0]` when the decorated function's qualname contains a dot — i.e. it was
defined in a class body — else use a module-level sentinel. Document the
limitation.)

### Edge cases

- **Per-instance timers are non-negotiable.** A naive closure-level timer means two
  widgets sharing one debounced method steal each other's pending calls.
- **WeakKeyDictionary + deleted QObjects:** the Python wrapper can outlive the C++
  object. Before firing, if the instance is a QObject, guard the call — the cheap
  way is `try: fn(*args) except RuntimeError: pass` scoped to the
  "wrapped C/C++ object has been deleted" case. Better: parent the QTimer to the
  instance when the instance IS a QObject (`QTimer(instance, singleShot=True)`) so
  Qt destroys the timer with the widget and the pending fire never happens.
- **Thread affinity:** QTimer must be created and started on a thread with an event
  loop. If the debounced fn can be called from worker threads, route the
  `timer.start` through `run_on_main` (item 1). Simplest v1: `assert_main_thread()`
  inside the wrapper with a clear error message; lift the restriction later.
- **Trailing vs leading:** debounce = trailing edge only (v1). Throttle = leading
  edge, plus one trailing fire carrying the last-seen args if calls arrived during
  the window (this is what UI code almost always wants — final state applies).
  Say which edges fire in each docstring; this is the #1 source of confusion.
- **Arguments:** last call wins, by design. Document it — someone will expect
  aggregation.
- **`@wraps` matters** — preserves name/docstring for the command palette and
  debugging.
- **Zero / negative msec:** treat as "call soon" (`QTimer.start(0)`), don't raise.

### Testing

pytest-qt with `qtbot.wait`: call a debounced counter 5 times in 50ms with a 100ms
debounce → after 200ms the count is 1 and the args are from call #5. Two instances
of the same class debounced independently. Deleted-widget case: create widget,
trigger debounce, `widget.deleteLater()`, process events, wait out the timer, no
crash.

---

## 4. Upstream Stagehand's `ApplicationUpdater` — `extras/updater/`

### Motivation

`Stagehand/src/stagehand/app_updater.py` is already qtstrap-shaped: it reads
`OPTIONS.app_info.AppReleaseUrl` and contains nothing Stagehand-specific. Every
distributed qtstrap app wants release checking.

### API

```python
from qtstrap.extras.updater import ApplicationUpdater

updater = ApplicationUpdater()               # reads OPTIONS.app_info
updater.update_found.connect(self.show_update_banner)
updater.check_latest()                       # async, via QNetworkAccessManager
menu.addAction(updater.check_for_updates_action())
```

`BaseAppInfo` in `options.py` gains an optional `RELEASE_URL: str` field (GitHub
API releases/latest endpoint). Keep the updater OUT of `BaseApplication.__init__` —
opt-in only.

### Implementation notes

Port the existing class nearly verbatim, with these mandatory fixes:

1. **Version comparison.** The current code does `float(d['tag_name'])` — this
   breaks the moment a tag is `1.10` (`1.10 < 1.9` as floats) or `v1.2.3` (raises).
   Replace with a tuple compare:

   ```python
   def parse_version(tag: str) -> tuple:
       tag = tag.lstrip('vV').split('-')[0].split('+')[0]   # v1.2.3-beta+build
       try:
           return tuple(int(p) for p in tag.split('.'))
       except ValueError:
           return ()    # unparseable -> never "newer"
   ```

   Compare `parse_version(remote) > parse_version(current)`. Tuples of different
   lengths compare correctly in Python (`(1, 10) > (1, 9)`, `(1, 2, 1) > (1, 2)`).

2. **Error handling.** The current code checks `reply.error()` but then assumes the
   body is valid JSON with a `tag_name` key. GitHub rate-limits unauthenticated API
   calls (60/hour/IP) and returns a JSON error body with **HTTP 403** — which is
   NOT a `QNetworkReply` error in all binding versions. Check the HTTP status
   attribute, wrap the JSON parse and key access in try/except, and emit a
   `check_failed = Signal(str)` instead of raising.

3. **`reply.deleteLater()`** in the finished handler — the current code leaks
   replies.

### Edge cases

- **Rate limiting yourself:** add an optional `check_interval_hours=24` — store the
  last check timestamp in QSettings and skip network entirely inside the window.
  `check_latest(force=True)` bypasses (for the menu action).
- **Redirects:** GitHub API URLs redirect occasionally; set
  `QNetworkRequest.FollowRedirectsAttribute` (or the qtpy equivalent —
  `RedirectPolicyAttribute` in Qt6). Test on both bindings if possible.
- **Missing config:** if `RELEASE_URL` is absent from AppInfo, `check_latest()`
  should log a warning and return, not raise — apps without releases will still
  construct the updater via copy-pasted code.
- **Offline:** a failed network check must be silent by default (log only).
  Nagging a user who is offline is worse than no updater.
- **Do NOT auto-download.** Scope = detection + signal. The app decides what to do.
- **Migration:** once merged, Stagehand's `app_updater.py` gets deleted and its
  import switched. Note in the PR that `AppReleaseUrl`/`AppVersion` attribute names
  in Stagehand's AppInfo must be reconciled with `BaseAppInfo`'s naming convention
  (`NAME`, `VERSION`, ... are upper-case there; pick `RELEASE_URL`).

### Testing

Unit-test `parse_version` exhaustively (`'1.10' > '1.9'`, `'v2.0'`, `'2.0.1-beta'`,
garbage → `()`). Network path: manual test against a real GitHub repo with an old
`VERSION`.

---

## 5. Single-instance guard — `utils/single_instance.py`

### Motivation

Apps like Stagehand (global keyboard hooks, OBS connections) must not run twice.
Classic bootstrap-framework feature.

### API

```python
# in main(), before BaseApplication:
from qtstrap import SingleInstance

guard = SingleInstance('stagehand')          # key defaults to AppInfo.NAME if None
if guard.already_running:
    guard.notify_running_instance(sys.argv)  # optional: pass argv over
    sys.exit(0)
...
guard.message_received.connect(window.handle_second_launch)  # activate window etc.
```

### Implementation

Two cooperating pieces:

- **`QLockFile`** at `Path(tempfile.gettempdir()) / f'{key}-{getpass.getuser()}.lock'`
  — `tryLock(0)` decides `already_running`. QLockFile has built-in stale-lock
  detection (dead PID → steals the lock), which is the whole reason to use it over
  a bare file.
- **`QLocalServer`/`QLocalSocket`** named `f'{key}-{getpass.getuser()}'` for the
  message channel. Winner calls `QLocalServer.removeServer(name)` then `listen(name)`;
  loser connects and writes newline-terminated JSON.

### Edge cases

- **Per-user keys.** Two different users on one machine must be able to run their
  own instance — hence the username suffix on both the lock path and socket name.
- **Stale socket on Unix:** after a crash the socket file lingers and `listen()`
  fails — that's what the `removeServer()` call before `listen()` is for. Never
  skip it.
- **Race window:** between the loser's failed `tryLock` and its socket connect, the
  winner may not be listening yet (still booting). Retry the connect 2–3 times over
  ~500ms before giving up; on total failure just exit silently (the instance
  exists; worst case the argv message is lost).
- **The message handler runs before the window exists** if the winner is slow to
  boot — buffer messages until a consumer connects to `message_received`, or
  document that the connect must happen before the event loop starts.
- **Lock lifetime:** keep the `SingleInstance` object referenced for the app's whole
  life (module global or attribute on the app). If it's GC'd, the lock releases and
  a second instance can start.
- **Frozen apps / portable mode:** temp-dir lock files work for both; do NOT put
  the lock in `config_dir` (a portable app on a USB stick used on two machines
  would deadlock itself with a stale-looking lock that isn't stale).
- **Don't make it automatic in `BaseApplication`** — some apps legitimately run
  multiple instances. Opt-in.

### Testing

Manual: launch the scratch app twice; second exits and the first's window raises.
Kill -9 the first; relaunch; confirm the stale lock is stolen and the app starts.

---

## 6. Crash dialog — `extras/log_monitor/crash_dialog.py`

### Motivation

The excepthook installed by `log_monitor.install()` already captures exceptions to
the database; the user-facing half is missing. Turns "the app just closed" reports
into pasteable tracebacks.

### API

```python
log_monitor.install(database_name, install_excepthook=True, crash_dialog=True)
```

### Implementation

Extend the existing `handle_exception` in `log_monitor/__init__.py`: after logging,
show a dialog with the exception summary, a collapsed full-traceback text area, a
**Copy details** button (traceback + app name/version + platform), and a link/path
to the log DB. Buttons: `Continue` (return, app may live) and `Quit`
(`os._exit(1)` — see below).

### Edge cases — this feature is 90% edge cases

- **Re-entrancy guard is mandatory.** If showing the dialog itself raises, you get
  an infinite excepthook loop. Module-level `_dialog_active` flag: if set, print
  to stderr and return immediately. Set it before constructing the dialog, clear
  after.
- **Wrap the entire dialog path in try/except** and fall back to the original
  stderr behavior. The excepthook must never raise.
- **No QApplication yet / already destroyed:** check `QApplication.instance()`;
  if None, stderr fallback. Crashes during import-time or during teardown must not
  try to build widgets.
- **`KeyboardInterrupt` must bypass the dialog** — check
  `issubclass(exc_type, KeyboardInterrupt)` and just chain to the default hook.
  Ctrl-C should stay Ctrl-C.
- **Exceptions on worker threads don't hit `sys.excepthook`** — they hit
  `threading.excepthook` (Python ≥3.8). Install a handler there too, and marshal
  the dialog to the main thread via `run_on_main` (item 1). Same for
  `sys.unraisablehook`? No — leave unraisable alone, it's noise.
- **Qt event loop state:** the excepthook fires between event-loop iterations (Qt
  swallows nothing in PySide6; slots that raise propagate to the hook). Running
  `dialog.exec()` starts a nested event loop, which generally works even from the
  hook — but the app state that caused the crash may make it fire again
  immediately. The re-entrancy guard converts that into stderr spam instead of a
  loop.
- **Quit button:** use `os._exit(1)`, not `sys.exit` / `app.quit()` — the app is
  in an arbitrary broken state, cooperative shutdown may hang or re-crash.
- **Flush the log DB first:** call `AsyncDatabaseHandler.force_flush()` before
  showing the dialog, so the exception row is on disk even if the user hard-kills.
- **Dialog copy should include** app name, version (`OPTIONS.app_info`), platform,
  Python and binding versions — five lines that save a whole triage round-trip.

### Testing

Scratch app with a menu action that raises `RuntimeError` (main thread) and another
that raises inside `threading.Thread` — both must produce the dialog exactly once.
A third action that raises inside the dialog's own show path (monkeypatch) — must
produce stderr output, not a loop.

---

## 7. `block_signals` context manager — `utils/block_signals.py`

### Motivation

The classic bug: loading settings into widgets re-fires all their `changed` signals
and triggers save/apply loops. Qt's `QSignalBlocker` handles one object and is
awkward from Python; the multi-widget with-statement version matches qtstrap's
ContextLayout aesthetic.

### API

```python
with block_signals(self.combo, self.slider, self.checkbox):
    self.combo.setCurrentIndex(2)
    self.slider.setValue(50)
```

### Implementation

```python
from contextlib import contextmanager


@contextmanager
def block_signals(*objects):
    """Temporarily block signals on any number of QObjects; restores prior state."""
    previous = [obj.blockSignals(True) for obj in objects]
    try:
        yield
    finally:
        for obj, prev in zip(objects, previous):
            obj.blockSignals(prev)
```

### Edge cases

- **Restore the *previous* state, not `False`.** `blockSignals(True)` returns the
  old value; nested blocks would otherwise unblock an outer block early. The sketch
  above already does this — keep it.
- **Exception safety:** the `finally` is the point. Don't get clever with early
  returns.
- **Deleted objects during the block:** `blockSignals` on a deleted wrapper raises
  RuntimeError in the finally; wrap the restore loop body in
  `try/except RuntimeError: pass`.
- **Blocked ≠ disconnected:** signals emitted while blocked are *lost*, not queued.
  Docstring must say this — it surprises people.
- Accept a single iterable too? No — variadic only. `block_signals(*widgets)`
  covers the list case and keeps the signature obvious.

### Testing

Pure unit test with pytest-qt: connect a counter to `QLineEdit.textChanged`, set
text inside the block (count unchanged), set after (count increments). Nested
blocks restore correctly.

---

## 8. Toast notifications — `widgets/toast.py`

### Motivation

Non-modal transient feedback ("Saved", "Update available", "Action fired") — every
app needs it, Qt has no built-in, and it belongs next to `toggle.py` in widgets.

### API

```python
from qtstrap import Toast

Toast.show_message(parent_window, 'Config saved')                       # info
Toast.show_message(parent_window, 'Connection lost', kind='error',
                   duration_ms=5000, action='Retry', on_action=self.reconnect)
```

### Implementation

A frameless child QWidget of the parent window (NOT a top-level window), styled
per-kind (`info`/`success`/`warning`/`error`), positioned bottom-right with a
margin, auto-dismissed by a single-shot QTimer, with opacity fade via
`QPropertyAnimation` on a `QGraphicsOpacityEffect`. A module-level manager keeps a
per-window list of live toasts and stacks them upward.

### Edge cases

- **Parent resize/move:** child-widget toasts move with the parent for free, but a
  resize requires repositioning — `installEventFilter` on the parent and reposition
  on `Resize`. This is the reason to prefer child widgets over frameless top-level
  windows (which need move tracking too, plus flicker on some WMs, plus taskbar
  quirks).
- **Stacking:** new toast while others are alive → position above them; when one
  dismisses, slide the ones above down (or simply reflow instantly — v1 can skip
  the slide animation).
- **Theme:** colors must come from the palette / `qtstrap.extras.style` colors, not
  hardcoded hex — the dark theme exists (`extras/style/dark_palette.py`). Test both
  themes.
- **Mouse:** hovering pauses the dismiss timer (restart on leave); clicking the
  body dismisses; the optional action button fires `on_action` then dismisses. Set
  `Qt.WA_TransparentForMouseEvents` **only** if you choose click-through — don't;
  hover-pause is more useful.
- **Timer/animation cleanup:** parent everything (timer, effect, animation) to the
  toast widget so `deleteLater` reaps it all. Guard the timeout slot against the
  widget already being deleted (deleteLater during fade).
- **Parent destroyed with live toasts:** they're children, Qt destroys them —
  but the manager's list must hold weak references or it leaks dead wrappers and
  crashes on the next reflow. Use `QObject.destroyed` to prune the list.
- **Threads:** `Toast.show_message` should call `run_on_main` (item 1) internally —
  toast-from-worker-callback is exactly the mistake people will make. Cheap
  insurance.
- **Multiple windows:** the manager keys its toast lists by parent window.

### Testing

Mostly manual/scratch-app (visual). Unit-testable pieces: stacking math, manager
pruning on destroy, thread marshaling (show from worker thread, no warnings).

---

## 9. `qtstrap.testing` — pytest fixtures for qtstrap apps

### Motivation

Downstream apps are nearly untestable today: `@singleton` holds global state across
tests, and `QSettings` writes to the real registry/ini. (Observed concretely:
Stagehand's new test suite carefully avoids importing anything Qt-touching.)
Making qtstrap apps testable compounds across every project.

**Depends on:** bugfix plan P2-10 (singleton rewrite keeps the `instances` dict
importable and clearable) and P0-1 (portable settings actually work, which is the
mechanism for settings isolation).

### API

```python
# conftest.py in a downstream app:
from qtstrap.testing import qtstrap_app, isolated_settings, reset_singletons  # noqa

def test_my_window(qtstrap_app):
    w = MyWindow()
    assert w.windowTitle() == 'My App'
```

Provide as important-to-copy documented fixtures (or a pytest plugin entry point —
v1: plain module the app's conftest re-exports).

### Implementation

```python
import pytest


@pytest.fixture(scope='session')
def qtstrap_app():
    """Session-scoped QApplication. Session-scoped because Qt allows exactly
    one QApplication per process, ever — even after deletion."""
    from qtpy.QtWidgets import QApplication
    app = QApplication.instance() or QApplication([])
    yield app
    # do NOT quit/delete — other session fixtures may still need it


@pytest.fixture(autouse=True)
def reset_singletons():
    from qtstrap.utils.singleton import instances
    instances.clear()
    yield
    instances.clear()


@pytest.fixture(autouse=True)
def isolated_settings(tmp_path, monkeypatch):
    """Point QSettings at a throwaway ini file per test."""
    from qtpy.QtCore import QSettings
    QSettings.setDefaultFormat(QSettings.Format.IniFormat)
    QSettings.setPath(QSettings.Format.IniFormat, QSettings.Scope.UserScope,
                      str(tmp_path))
    yield
```

### Edge cases

- **QApplication is once-per-process, forever.** Even `del app` +
  gc doesn't allow a second one under PySide6. Session scope, never teardown, and
  tolerate a pre-existing instance (pytest-qt users already have one — detect and
  reuse; the fixture must compose with pytest-qt's `qapp`, not fight it).
- **`BaseApplication` is harder than `QApplication`:** it requires `AppInfo` and
  runs theme application. For v1, the fixture builds a plain `QApplication` and a
  separate `qtstrap_appinfo` fixture monkeypatches `OPTIONS.app_info` /
  `OPTIONS.config_dir` (→ `tmp_path`) for code that reads OPTIONS directly. Do NOT
  attempt to construct `BaseApplication` in the fixture — its `__init__` calls
  `QSettings()` and `apply_theme`, which drag in the icon path and AppDirs; too
  much machinery for a unit-test fixture.
- **Settings isolation has a hole:** modules that captured a `QSettings` *instance*
  (not the class) at import time keep their old target. The `setPath` +
  `setDefaultFormat` approach covers the standard `QSettings()` constructor calls,
  which is what qtstrap code does. Document the hole.
- **`instances.clear()` does not destroy QObject singletons** — it only forgets
  them. A singleton widget from test A still exists (parentless) when test B
  creates a fresh one; usually harmless, but global side effects (installed event
  filters, `App().aboutToQuit` connections) leak across tests. Document; offer
  `reset_singletons(deep=True)` later if it bites (calls `deleteLater` on QObject
  instances and processes events).
- **Timers/deferred calls leaking between tests:** qtstrap's `call_later` keeps a
  module list of timers. Add a `flush_call_later()` helper to the testing module
  (process events until the `_call_timers` list is empty, with a deadline).
- **Headless CI:** Qt needs a display; document `QT_QPA_PLATFORM=offscreen` in the
  module docstring — it's the difference between "works on my machine" and CI.
- **pytest-qt interop:** if pytest-qt is installed, prefer its `qapp`/`qtbot`; our
  `qtstrap_app` should just depend on `qapp` when available. Detect via
  `importlib.util.find_spec('pytestqt')`.

### Testing

Meta but real: a test that uses two singletons and asserts they're fresh per test
(two tests sharing a module-level list of ids). A test that writes QSettings and a
sibling test asserting the key is absent.

---

## Suggested order & packaging

| Order | Item | Depends on |
|-------|------|------------|
| 1 | §1 thread marshaling | — |
| 2 | §3 debounce/throttle | §1 (optional) |
| 3 | §2 run_in_thread | §1 |
| 4 | §7 block_signals | — (trivial, any time) |
| 5 | §9 testing module | bugfix P2-10, P0-1 |
| 6 | §4 updater | — |
| 7 | §5 single instance | — |
| 8 | §6 crash dialog | §1 |
| 9 | §8 toast | §1, style/themes |

§1–3 + §7 are one minor release ("concurrency kit"). §9 unlocks testing everything
after it — worth pulling forward if the bugfix plan lands first. Version bump:
minor (new API, no breaking changes; the singleton rewrite in the bugfix plan is
the only behavioral change and it preserves the documented contract).
