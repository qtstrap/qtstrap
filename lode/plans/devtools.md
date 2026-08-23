---
type: plan
status: idea
tags: [plan, devtools, debug-port, scene-tree, inspector, repl, style-editor, http, agent]
keywords: [devtools, debug port, http server, scene tree, inspector, repl, style editor, agent control, qt devtools, control port]
summary: Qt devtools system — in-app dock widgets (scene tree, inspector, style editor, REPL) plus an agent-friendly HTTP debug control port. Shared backend, two transports.
---

# Plan: Qt Devtools

## Context

qtstrap has the pieces of a Qt devtools panel: a scene tree viewer
(`extras/devtools/scene_tree.py`), an inspector, a style editor, and a REPL
stub. These are in-app dock widgets for a human looking at the screen. They share
backend logic (QObject tree walking, property extraction) but each implements
it independently with no reusable extraction layer.

At work, the author embedded debug HTTP servers into IDE extensions for agent
access. The same pattern applied to Qt gives agents remote access to a running
app's live state — inspect widgets, read properties, push style changes, eval
code, tail logs — without a human in the loop.

This plan covers the **entire devtools system**: fixing the existing in-app
widgets, extracting shared backend logic, and adding the HTTP control port as
a parallel transport.

Related: [../async-guide.md](../async-guide.md) §5 (BaseApplication packaging —
devtools as a declarative flag), [new-utilities.md](new-utilities.md) §1
(`run_on_main_sync` — the marshaling primitive the HTTP server needs),
[bugfix-review-2026-07.md](bugfix-review-2026-07.md) P2-15 (scene tree bugs).

---

## 1. Existing state

### Scene tree (`scene_tree.py`)
- `TreeNode` walks the QObject tree, installs event filters for child
  add/remove and show/hide. Maintains a class-level `inverse` dict mapping
  QObject → TreeNode for reverse lookup.
- `SceneTreeWidgetItem` displays objectName (or `<ClassName>`), visibility icon.
- `SceneTree` (QTreeWidget) handles click (inspect), icon click (toggle
  visibility), context menu.
- `SceneTreeDockWidget` wraps it, scans on a 2-second `call_later`.

**Bugs (P2-15):**
- `TreeNode.inverse` never cleared — `destroyed` signal is commented out. Rescan
  produces a nearly empty tree because `scan()` skips objects still in `inverse`.
  Dead QObjects leak for the app's lifetime.
- `contextMenuEvent` doesn't check for `None` — right-clicking empty space crashes.
- 'Open REPL' and 'Edit Style' context menu actions are unconnected no-ops.
- `qtpy.shiboken` import breaks under PyQt (only exists under PySide).
- `qcolors.white` foreground on named items is invisible on light theme.

### Inspector (`inspector.py`)
- Shows objectName, type, base type (first QtWidgets class in MRO).
- `inspect(item)` sets QLabel text directly — no reusable data extraction.

### Style editor (`style_editor.py`)
- Monaco-based QSS editor, persists to QSettings, applies to parent widget.
- Depends on `monaco` package — heavy, optional at best.
- Only edits the parent widget's stylesheet, not per-widget.

### REPL (`repl.py`)
- Stub. A QLabel saying 'REPL'. Not functional.

---

## 2. Design

### Two transports, one backend

The in-app dock widgets and the HTTP control port are two front-ends for the
same backend. Extract the shared logic into reusable functions that return plain
data (dicts, lists), not Qt widget mutations.

```
┌─────────────────────────────────────────────┐
│               Backend (pure)                 │
│  collect_widget_info(obj) -> dict            │
│  dump_scene_tree(root) -> list[dict]         │
│  set_widget_style(obj, qss) -> None          │
│  set_widget_property(obj, name, value)       │
│  eval_in_app(code) -> Any                    │
│  tail_logs(limit) -> list[dict]              │
└──────────┬──────────────────┬───────────────┘
           │                  │
     ┌─────┴─────┐     ┌──────┴──────┐
     │  In-app   │     │  HTTP port  │
     │  docks    │     │  (agents)   │
     └───────────┘     └─────────────┘
```

The in-app docks format the dict into widgets. The HTTP handlers serialize it
to JSON. Both call the same backend functions on the main thread.

### Backend functions

```python
def collect_widget_info(obj: QObject) -> dict:
    """Extract widget metadata, properties, geometry, and state as a dict."""
    # Refactored from Inspector.inspect()
    # Returns: {objectName, className, baseType, visible, geometry, 
    #           properties: {name: value}, signals: [name, ...], 
    #           stylesheet: str, children: [objectName, ...]}

def dump_scene_tree(root: QObject) -> list[dict]:
    """Walk the QObject tree from root, return nested JSON."""
    # Uses the same walk logic as TreeNode.scan()
    # Each node: {objectName, className, visible, children: [...]}

def set_widget_style(obj: QObject, qss: str) -> None:
    obj.setStyleSheet(qss)

def set_widget_property(obj: QObject, name: str, value) -> None:
    obj.setProperty(name, value)

def eval_in_app(code: str, namespace: dict = None) -> Any:
    """Eval code in the app's namespace on the main thread."""
```

### In-app dock refactoring

- **Scene tree:** fix the `inverse` leak (P2-15), clear on rescan, re-enable
  `destroyed` hookup with `isValid` guards. Fix `qtpy.shiboken` import with
  `qtpy.API_NAME` guard for PyQt. Fix `contextMenuEvent` None crash. Wire the
  'Open REPL' and 'Edit Style' menu actions to the actual dock widgets. Fix
  `qcolors.white` → use palette text color.
- **Inspector:** call `collect_widget_info(obj)` and format the dict into
  labels instead of setting them directly. Show properties, geometry, signals
  — not just name/type/baseType.
- **Style editor:** make Monaco optional (fall back to `QPlainTextEdit` or the
  `CodeEditor` from `extras/code_editor`). Support per-widget style editing,
  not just the parent. Use `collect_widget_info` to show current stylesheet.
- **REPL:** implement a functional REPL. A `QPlainTextEdit` for input, a
  `QTextEdit` for output, `exec`/`eval` in a namespace that includes
  `QApplication.instance()`, `QApplication.topLevelWidgets()`, and the app
  module. History with up/down arrows.

### HTTP control port

Stdlib `http.server` in a thread. All Qt access via `run_on_main_sync`.

#### Endpoints

| Method | Path | Body | Returns |
|--------|------|------|---------|
| GET | `/scene` | | Full QObject tree as nested JSON |
| GET | `/scene/<objectName>` | | Widget info (properties, geometry, signals, style) |
| GET | `/scene/<objectName>/children` | | Direct children list |
| GET | `/scene/<objectName>/properties` | | All readable properties |
| POST | `/scene/<objectName>/style` | `{"style": "..."}` | Set stylesheet |
| POST | `/scene/<objectName>/property` | `{"name": "...", "value": ...}` | Set property |
| POST | `/scene/<objectName>/visible` | `{"visible": bool}` | Show/hide |
| POST | `/scene/<objectName>/click` | `{}` | Simulate click |
| POST | `/eval` | `{"code": "..."}` | Eval result or error |
| GET | `/logs?limit=100` | | Recent log records |
| GET | `/logs?level=ERROR` | | Filtered logs |
| GET | `/settings` | | All QSettings keys/values |
| GET | `/settings/<key>` | | Single setting |
| POST | `/settings/<key>` | `{"value": ...}` | Set setting |
| GET | `/app` | | App name, version, theme, uptime |
| GET | `/app/widgets` | | Flat list of all live widgets |

Custom endpoints: apps register handlers via `DevtoolsServer.register(path, fn)`.

#### Security

- Bind to `127.0.0.1` only.
- Optional `DEVTOOLS_TOKEN` — if set, requests need `Authorization: Bearer`.
- `/eval` requires separate `DEVTOOLS_EVAL=True` flag.

---

## 3. Integration with BaseApplication

### Phase 1: Explicit opt-in

```python
from qtstrap.extras.devtools import DevtoolsServer

devtools = DevtoolsServer(port=8765)
devtools.start()
```

### Phase 2: Declarative flag (ties into async-guide §5)

```python
class Application(BaseApplication):
    DEVTOOLS = True

app = Application()
app.run()  # devtools starts as part of run()
```

Server shuts down in `aboutToQuit`.

---

## 4. Open questions

- **WebSocket vs HTTP:** HTTP is simpler for agents. WebSocket gives push for
  scene tree changes. Start HTTP, add WS later.
- **Scene tree change notifications:** `TreeNode.eventFilter` already detects
  child add/remove and show/hide. Could expose `/scene/watch` (SSE). Low priority.
- **Persistent REPL sessions:** `/eval` is stateless per call. A persistent REPL
  maintaining namespace across calls needs session management. Defer.
- **Monaco dependency:** make optional. Fall back to `CodeEditor` or `QPlainTextEdit`.
- **`qtpy.shiboken` vs PyQt:** scene tree uses `isValid`/`delete` from shiboken,
  which doesn't exist under PyQt. Need a `qtpy.API_NAME` guard or a compat shim.

---

## 5. Implementation order

1. **Fix scene tree bugs (P2-15):** clear `inverse` on rescan, re-enable
   `destroyed` hookup, fix `contextMenuEvent` None crash, fix `qtpy.shiboken`
   import, fix `qcolors.white`. Wire menu actions.
2. **Extract `collect_widget_info(obj) -> dict`** from `Inspector.inspect()`.
   Refactor inspector to call it and format the dict.
3. **Extract `dump_scene_tree(root) -> list[dict]`** from `TreeNode.scan()`.
   Refactor scene tree to call it and build items from the dict.
4. **Implement the REPL** — functional `exec`/`eval` with history.
5. **Make Monaco optional** in style editor — fall back to `CodeEditor`.
6. **`run_on_main_sync`** (from new-utilities §1) — prerequisite for HTTP server.
7. **`DevtoolsServer` + `/scene` + `/scene/<name>`** — minimal viable port.
8. **`/eval`** — requires `DEVTOOLS_EVAL` flag.
9. **`/logs`** — query the log database.
10. **`/settings` + `/app`** — introspection.
11. **Mutation endpoints** — style, property, visible, click.
12. **Declarative flag integration** — wire into BaseApplication.