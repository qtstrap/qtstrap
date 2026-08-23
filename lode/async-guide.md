---
type: domain
tags: [guide, async, promises, asyncio, qt]
keywords: [async, promises, asyncio, Qt, qtasyncio, qasync, promisio, signals, slots]
summary: How qtstrap applications get async capability without converting to async as a programming model.
---

# Async Interop Guide: asyncio, Promises, and Qt

How qtstrap applications get async *capability* without converting to async as a
programming model. This is part design rationale, part proposal, part
implementation guide — it includes the thought process on purpose, so that anyone
(human or model) implementing pieces of it understands *why* the design looks the
way it does and doesn't "improve" it into something else.

Related plans: [plans/new-utilities.md](plans/new-utilities.md) (§1 `run_on_main`
is a dependency of several pieces here), [plans/bugfix-review-2026-07.md](plans/bugfix-review-2026-07.md).

---

## 1. Ground rules (the thought process)

### Signals/slots stays the primary model

Every app in the fleet is already a single-threaded, event-driven, run-to-completion
system: Stagehand and DeviceManager use `QWebSocket`/`QWebSocketServer` for all
network I/O, codex wraps serial the same way, and state lives in plain member
variables. This is the embedded superloop model and it is *not* a limitation to be
engineered away — it's the reason these apps are debuggable. Async is being added
as a **capability at the edges**, not a new paradigm.

### Why promises and not async/await as the interface

The decisive observation: **promises are the async model that is signals-shaped.**

- `.then(cb)` is a single-shot connection to a "finished" event
- `.catch(cb)` is a connection to an error signal
- A promise is morally a one-shot QObject with `resolved`/`rejected` signals plus
  chaining sugar

Whereas `async/await` is *control-flow*-shaped: it wants to own the structure of
your functions, and it colors every caller (`async` propagates up call chains).
In a signals codebase, awaits are a foreign body; thens are just more callbacks.

Two Python-specific reasons promises fit better here:

1. **Eager vs lazy.** Python coroutines are lazy — calling `async def` produces an
   inert object, and forgetting to `await`/`create_task` it means it silently never
   runs. This is the asyncio ecosystem's #1 footgun. JS-style promises are eager —
   calling the function starts the work. `promisify` imports that eagerness: a
   promisified function can be connected **directly to a Qt signal** and it just
   works, because the call itself schedules the task:

   ```python
   button.clicked.connect(obs.refresh_scenes)   # works; no await, no wrapper
   ```

2. **Combinators.** Signal composition is Qt's genuine weak spot. "Fire when all
   three of these finish" or "first of these wins" requires hand-rolled counters
   and careful disconnect logic, and this problem has actually occurred in these
   apps. `Promise.all` / `race` / `any` / `allSettled` solve it for free. This is
   the single strongest argument for a promise layer over signals-only.

### The library: promisio

Miguel Grinberg's `promisio` provides JS-semantics promises over asyncio: eager,
task-backed (so `.cancel()` works), `.then/.catch/.finally`, and the JS combinator
set. It is small and quietly maintained — the correct response to which is to
**vendor it** (the same move as Roadie in Stagehand), or pin it and accept the
tiny risk. Do not fork-and-diverge; keep it verbatim so upstream fixes can be
copied in.

### The boundary rule

> `async`/`await` syntax is allowed **only inside service objects** (the "island").
> Everything a service exposes is a promisified method. The rest of the app
> consumes promises with `.then/.catch` or connects them to signals, and never
> writes `await`.

This keeps the blast radius of asyncio at exactly one class per integration, the
same way you'd wrap a vendor RTOS task behind a message-queue API.

---

## 2. The event loop decision

Promises still need a running asyncio loop. The trick is to treat the loop as
**ambient plumbing** (like a browser's event loop — always there, never managed),
not as a programming model. That means a merged Qt/asyncio loop on the main
thread.

Two implementations:

| | `PySide6.QtAsyncio` | `qasync` |
|---|---|---|
| Maintenance | First-party (Qt Company) | Community (quamash → asyncqt → qasync lineage) |
| Bindings | **PySide6 only** | PyQt5/6, PySide2/6 (qtpy-compatible) |
| Loop fundamentals (tasks, timers, futures) | Yes | Yes |
| Socket APIs (`add_reader`, `create_connection`) | **Historically missing** — verify per release | Yes (via `QSocketNotifier`) |
| Status | Technical preview | Battle-tested |

**DeviceManager already runs QtAsyncio as its main loop today**
(`QtAsyncio.run(handle_sigint=True)` in `src/main.py`), and it works because the
app's networking is all Qt-native — nothing needs asyncio sockets.

**Decision rule:** stay on QtAsyncio while the async island contains only
coroutine orchestration (dialog flows, sequencing, timers, promisified logic).
The moment an asyncio-only *networking* library becomes necessary (aiohttp, the
`websockets` package), QtAsyncio's socket gap becomes fatal and the loop must
switch to qasync. Verify the gap against the installed PySide6 before believing
either claim:

```python
# scratch check: does the merged loop support asyncio networking?
import asyncio

async def probe():
    try:
        reader, writer = await asyncio.open_connection('example.com', 80)
        writer.close()
        print('socket APIs: supported')
    except NotImplementedError:
        print('socket APIs: NOT supported on this loop')
```

Since Qt-native I/O (`QWebSocket` etc.) is the fleet's default anyway, the
expected steady state is: QtAsyncio, no asyncio networking, promises for
orchestration and combinators.

**Consequence for qtstrap:** QtAsyncio is PySide6-only, which conflicts with
qtstrap's qtpy neutrality. The integration (see §5) must lazy-import and raise a
clear error under PyQt (`'ASYNC support currently requires PySide6, or install
qasync'`) rather than break the package for other bindings.

---

## 3. The promise layer: `qtstrap.extras.promise`

Proposed module contents, each with rationale and edge cases.

### 3.1 The vendored core

`extras/promise/_promisio.py` — vendored copy, untouched.
`extras/promise/__init__.py` — re-exports `Promise`, `promisify`, plus the
qtstrap-specific helpers below.

### 3.2 Service island example

The canonical shape, using an OBS-flavored service. Note the service *internally*
may still be built on `QWebSocket` — promises don't require asyncio I/O; a promise
can resolve from a plain Qt slot:

```python
from qtstrap.extras.promise import Promise, promisify


class ObsService(QObject):
    """The async island. `async def` is legal in here and nowhere else."""

    @promisify
    async def get_scene_list(self) -> list[str]:
        response = await self._request('GetSceneList')      # island-internal
        return [s['sceneName'] for s in response['scenes']]

    @promisify
    async def go_live(self):
        # linear multi-step flow with one error boundary — the thing that
        # would be a 5-state enum as pure signals
        await self._request('SetCurrentProgramScene', scene='Starting Soon')
        await asyncio.sleep(2.0)
        await self._request('StartStream')
        await self._request('SetCurrentProgramScene', scene='Live')
```

Consumers never await:

```python
class Dashboard(QWidget):
    def refresh(self):
        obs.get_scene_list() \
            .then(self.populate_scene_buttons) \
            .catch(self.show_error)
```

### 3.3 Combinators (the actual motivating problem)

"Build the dashboard once scenes, sources, AND profile have all arrived":

```python
Promise.all([
    obs.get_scene_list(),
    obs.get_source_list(),
    obs.get_current_profile(),
]).then(lambda results: self.build_dashboard(*results)) \
  .catch(self.show_error)
```

For contrast, the signals-only version of this — a counter, three result slots,
three error paths, and a reset method for retries — is ~30 lines of accounting
per occurrence. `Promise.race` (first wins, e.g. response-vs-timeout) and
`Promise.allSettled` (collect successes AND failures, e.g. probing N devices)
cover the other recurring shapes. codex device enumeration is a natural
`allSettled` consumer.

### 3.4 `wait_for_signal` — awaiting Qt from the island

The inverse bridge: island code that needs to wait for a Qt event.

```python
def wait_for_signal(signal, *, timeout: float | None = None):
    """Return an awaitable that resolves with the signal's arguments.

    Single-shot: disconnects itself after the first emission.
    """
    loop = asyncio.get_event_loop()
    future = loop.create_future()

    def handler(*args):
        signal.disconnect(handler)
        if not future.done():
            future.set_result(args[0] if len(args) == 1 else args or None)

    signal.connect(handler)

    if timeout is not None:
        return asyncio.wait_for(future, timeout)
    return future
```

**Edge cases:**
- Multi-arg signals resolve with a tuple; single-arg with the bare value;
  zero-arg with None. Document this — it's a convention, not an inevitability.
- If the signal's owner is destroyed before emitting, the future never resolves.
  For long waits, also connect `owner.destroyed` to
  `future.set_exception(RuntimeError(...))` — offer an `owner=` kwarg.
- The disconnect-inside-handler pattern is safe in Qt (the emission in progress
  completes), but do not convert this to a persistent connection.
- `future.done()` guard matters: timeout cancellation can race the emission.

### 3.5 AwaitableDialog, fixed and simplified

The existing `widgets/awaitable_dialog.py` hand-rolls an `asyncio.Event` and has
a real bug: **Esc or the window-close button triggers `QDialog.reject()`, the
event never sets, and the awaiting coroutine hangs forever.** The fix is to await
the signal Qt already provides — `finished(int)` fires for accept, reject, Esc,
and X uniformly:

```python
class AwaitableDialog(QDialog):
    def submit(self, result=None):
        self._result = result
        self.accept()

    def __await__(self):
        self.open()                       # NOT exec() — no nested event loop
        yield from wait_for_signal(self.finished).__await__()
        self.deleteLater()
        return getattr(self, '_result', None)   # None on reject/Esc/X
```

Note `open()` not `exec()`: `exec()` spins a **nested event loop**, which is the
Qt equivalent of enabling interrupts inside an ISR — re-entrancy in the middle of
whatever slot showed the dialog. The promise/coroutine version exists precisely
to get linear-reading dialog flow *without* that. Never mix the two.

### 3.6 Lifetime binding — recovering Qt's auto-disconnect

Signals die with their QObject; promise callbacks don't. A `.then(self.populate)`
holds `self` past widget destruction, and firing it raises on a dead wrapper.
Restore the Qt property explicitly:

```python
def owned_by(promise, owner: QObject):
    """Cancel the promise when its consumer is destroyed."""
    owner.destroyed.connect(lambda *_: promise.cancel())
    return promise
```

```python
owned_by(obs.get_scene_list().then(self.populate), self)
```

**Edge cases:** promisio promises are task-backed so `.cancel()` cancels the
underlying task; a cancelled promise must not invoke `.catch` handlers with
`CancelledError` in a way that spams the error UI — the default rejection handler
(§3.7) should swallow `CancelledError` specifically. If the promise settles
before the owner dies, the lingering `destroyed` connection calls `.cancel()` on
a settled promise — a no-op, harmless.

### 3.7 Default rejection handler — day-one requirement

Unhandled promise rejections are Python's "task exception was never retrieved"
wearing a different hat: invisible until loop shutdown, then a wall of noise.
Install a policy when the loop starts:

```python
def _handle_async_exception(loop, context):
    exc = context.get('exception')
    if isinstance(exc, asyncio.CancelledError):
        return                                   # lifecycle noise, not an error
    logging.getLogger('async.unhandled').error(
        context.get('message', 'unhandled async exception'),
        exc_info=exc,
    )

loop.set_exception_handler(_handle_async_exception)
```

Routing to `logging` means rejections land in the log monitor next to everything
else. Project rule regardless: user-facing chains end in `.catch`; the handler is
the safety net, not the plan.

---

## 4. What this replaces

- The previously-shelved `extras/aio` background-thread idea
  ([plans/new-utilities.md](plans/new-utilities.md) discussion): superseded for
  the current fleet, because all I/O is Qt-native and the merged loop suffices.
  The background-thread quarantine remains the documented fallback if a
  *blocking or asyncio-socket-dependent* library must be integrated while staying
  on QtAsyncio.
- `promisify`-per-app scratch experiments (Stagehand `async_test.py`): the guide
  + `extras/promise` is the packaged version.

---

## 5. Packaging onto BaseApplication

### 5.1 The evidence: what every app hand-rolls today

Comparing `Stagehand/src/stagehand/application.py` and
`DeviceManager/src/application.py`:

| Boilerplate | Stagehand | DeviceManager | qtstrap answer today |
|---|---|---|---|
| `log_monitor.install()` + custom exception logger name | yes | yes | manual |
| Plugin loader instantiation | yes | yes | none (per-app) |
| codex `DeviceManager(self)` + `aboutToQuit.connect(close)` | yes | yes | manual |
| Update checker | yes (local `app_updater.py`) | no | none (upstream per utilities plan §4) |
| Style/theme setup | via qtstrap | **hand-rolled** (`setStyle('Fusion')` + own dark palette) | exists but was bypassed |
| Entry point (`main()`/`run()`) | hand-rolled | hand-rolled (`QtAsyncio.run`) | template only |
| beartype install | no | yes (in `main.py`) | none |
| Event-loop profiler (`notify()` timing) | no | written but commented out | none |

DeviceManager bypassing the theme system is itself a finding: when the framework's
feature isn't quite right, apps quietly reimplement it — the strongest possible
signal about what BaseApplication should absorb properly.

### 5.2 The design: declarative flags, lazy assembly

BaseApplication already established the pattern with `AppInfo`: **the subclass
declares, the base class assembles.** Extend that instead of inventing a config
system:

```python
class Application(BaseApplication):
    class AppInfo:
        NAME = 'Stagehand'
        VERSION = '0.5'
        PUBLISHER = 'DaelonCo'
        ICON_PATH = 'resources/stagehand.ico'
        RELEASE_URL = 'https://api.github.com/repos/DaelonSuzuka/Stagehand/releases/latest'

    LOG_MONITOR = True          # log_monitor.install(), exception logger named after app
    CRASH_DIALOG = True         # extras crash dialog (utilities plan §6)
    SINGLE_INSTANCE = True      # lock + activate-existing (utilities plan §5)
    UPDATER = True              # requires AppInfo.RELEASE_URL (utilities plan §4)
    ASYNC = True                # merged loop + promise runtime (this guide)
```

And the entry point collapses to:

```python
def main():
    app = Application()
    window = MainWindow()
    window.show()
    app.run()                   # <- the important new method
```

### 5.3 Why `run()` is the keystone

The async loop *changes the exec call*: plain apps call `app.exec()`,
QtAsyncio apps call `QtAsyncio.run()`, qasync apps build a `QEventLoop` and
`run_forever()` inside a context manager. Today each app hand-rolls this choice
in its own `main()` — which is exactly why loop-related boilerplate can't
currently be packaged. Once BaseApplication owns the exec call, it can own
everything that must wrap it:

```python
class BaseApplication(QApplication):
    ASYNC: bool | str = False   # False | True ('auto') | 'qtasyncio' | 'qasync'

    def run(self):
        if not self.ASYNC:
            return self.exec_()

        backend = self._resolve_async_backend()   # availability + binding checks
        if backend == 'qtasyncio':
            import PySide6.QtAsyncio as QtAsyncio
            self._install_async_exception_handler()
            # handle_sigint must stay False: it is literally
            # signal.signal(SIGINT, SIG_DFL), which clobbers BaseApplication's
            # graceful SIGINT/SIGTERM handlers with immediate death
            return QtAsyncio.run(handle_sigint=False)
        if backend == 'qasync':
            import qasync, asyncio
            loop = qasync.QEventLoop(self)
            asyncio.set_event_loop(loop)
            self._install_async_exception_handler()
            with loop:
                return loop.run_forever()
```

**Edge cases:**
- `ASYNC = True` resolves: PySide6 → qtasyncio; other bindings → qasync if
  installed, else a clear ImportError naming both options. Never crash with a
  bare ModuleNotFoundError from deep inside Qt.
- `run()` must remain **optional**: existing apps calling `app.exec_()` directly
  keep working forever. `run()` with all flags False is exactly `exec_()`.
- qasync should be an optional extra: `pip install qtstrap[async]`. QtAsyncio
  ships with PySide6 — no extra needed.
- The async exception handler (§3.7) is installed by `run()`, not at import.

### 5.4 What each flag does, and ordering

Assembly happens in `__init__` (after the existing AppInfo/dirs/theme sequence)
except where noted. Order matters and is fixed:

0. **Signal handlers** — *implemented (2026-07)*: `INSTALL_SIGNAL_HANDLERS = True`
   (opt-out class attr, deliberately default-on unlike the flags below — it
   restores the old unconditional `install_ctrlc_handler` behavior, modernized:
   `set_wakeup_fd` + `QSocketNotifier` instead of the 10ms polling timer, and
   covers SIGTERM so logout/kill runs the graceful quit path). Once the
   shutdown pipeline (item 6) lands, signal-quit flows through it for free.
1. **Main-thread dispatcher** (utilities plan §1) — *always on, not a flag.*
   Created first so every later subsystem can rely on `run_on_main`. Costs one
   idle QObject.
2. **`SINGLE_INSTANCE`** — must run as early as possible, *before* heavy
   subsystems spin up, so a duplicate launch exits cheaply. If already running:
   send argv to the incumbent and `sys.exit(0)` — document loudly that
   `__init__` can terminate the process when this flag is set.
3. **`LOG_MONITOR`** — `log_monitor.install(database_name=...)` with
   `exception_logger_name = f'{AppInfo.NAME.lower()}.exceptions'` (both apps set
   exactly this by hand today).
4. **`CRASH_DIALOG`** — extends the excepthook installed by 3; requires 3.
5. **`UPDATER`** — construct `ApplicationUpdater` as `self.updater`, do NOT
   auto-check (apps decide when); warn-and-skip if `RELEASE_URL` is absent.
6. **Shutdown pipeline** — *always on*: a `self.on_shutdown(callable, priority=0)`
   registry flushed on `aboutToQuit` in priority order. Both apps' manual
   `aboutToQuit.connect(self.device_manager.close)` becomes
   `app.on_shutdown(self.device_manager.close)`, and qtstrap's own teardown
   (flush log DB, cancel promises, stop dispatchers) registers at low priority so
   it runs *after* app callbacks.
7. **`ASYNC`** — mostly resolved in `run()` (§5.3); `__init__` only records the
   flag and prepares the promise runtime import.

Candidates deliberately **not** flags:
- **Plugin loading** — both apps have one, but the discovery logic is genuinely
  app-specific. Reconsider only if a third app duplicates one of the existing two.
- **beartype claw** — must run before app modules import, i.e. above
  BaseApplication's pay grade; belongs in `main.py`. A doc note, not a feature.
- **Event profiler** (DeviceManager's commented-out `notify()` timing) — useful,
  but belongs in `extras/devtools` as an opt-in mixin or env-var switch
  (`QTSTRAP_PROFILE_EVENTS=1`), not a permanent `notify()` override: overriding
  `notify()` adds a Python call to *every event in the application*, measurably.

### 5.5 Interaction with testing

Every flag defaults **False** precisely so `qtstrap.testing` (utilities plan §9)
can construct app objects without side effects — a test app must never grab a
single-instance lock, install excepthooks, or open a log database unless the test
asks for it. The always-on pieces (dispatcher, shutdown registry) are inert
without an event loop and safe in tests. This default-off posture is also the
backwards-compatibility story: an existing subclass that sets no flags gets
byte-for-byte today's behavior.

### 5.6 Adoption order

1. Land `run()` + dispatcher + shutdown pipeline (no behavior change for anyone).
2. Convert **DeviceManager** first — it's already on QtAsyncio, so `ASYNC = True`
   plus deleting its hand-rolled `main()` glue is a pure simplification. Its
   hand-rolled style init should move onto the theme system at the same time
   (fix the `themes.py` TODOs from the bugfix plan first).
3. Convert Stagehand: flags + upstreamed updater (utilities plan §4) delete
   `app_updater.py` and most of `Application.__init__`.
4. Only then advertise the flags in qtstrap docs/template.

---

## 6. Quick reference: the rules

1. Signals/slots is the primary model; async is a capability, not a conversion.
2. `async`/`await` only inside service objects. Consumers use `.then/.catch`.
3. The loop is ambient plumbing, owned by `BaseApplication.run()`.
4. Qt-native I/O (`QWebSocket` etc.) remains the default; asyncio networking is
   the exception and forces the qasync backend.
5. Every promise chain a user can trigger ends in `.catch`; the loop exception
   handler is the net, not the plan.
6. The awaitable dialog pattern (`result = await ConfirmDialog()`, inspired by
   [NiceGUI's dialog `__await__`](https://daelon.dev/posts/nicegui_dialogs/))
   is the motivating use case for the promise layer. The existing
   `AwaitableDialog` widget has the right shape but is broken — `show()` instead
   of `open()`, and `asyncio.Event` that never fires on Esc/close. §3.5's fix
   (`wait_for_signal(self.finished)`) is the correct implementation, and should
   be the first example in the docs once `run()` + the promise runtime land.
7. Promises consumed by widgets get `owned_by(promise, widget)`.
8. `dialog.open()` + await/then, never `dialog.exec()` from async-adjacent code.
9. Vendor promisio; don't fork it.
