---
type: plan
status: idea
tags: [plan, devtools, debug-port, scene-tree, http, agent]
keywords: [devtools, debug port, http server, scene tree, inspector, repl, agent control, qt devtools, control port]
summary: Agent-friendly debug control port for Qt apps — embedded HTTP server exposing live widget tree, property inspection, style manipulation, eval, and log tailing.
---

# Plan: Qt Devtools Control Port

## Context

qtstrap already has the pieces of a Qt devtools panel: a scene tree viewer
(`extras/devtools/scene_tree.py`), an inspector, a style editor, and a REPL
stub. These are in-app dock widgets for a human looking at the screen. An agent
(or a developer with curl) can't use them.

At work, the author has been embedding debug HTTP servers into IDE extensions.
The same pattern applied to Qt gives agents remote access to a running app's
live state — inspect widgets, read properties, push style changes, eval code,
tail logs — without a human in the loop.

The scene tree's `TreeNode.inverse` dict already maintains a QObject-to-node
registry. The log database is already queryable. The inspector already extracts
type/property info. The debug port is a new transport for existing capability.

Related: [../async-guide.md](../async-guide.md) §5 (BaseApplication packaging —
devtools as a declarative flag), [new-utilities.md](new-utilities.md) §1
(`run_on_main_sync` — the marshaling primitive the HTTP server needs).

---

## 1. Goal

An embedded HTTP server that lets an agent inspect and manipulate a running Qt
application's live state. Not a production web server — a debug tool. One agent
or one developer at a time.

Design priorities, in order:
1. **Safe by default.** The server is off unless explicitly enabled. No
   unauthenticated remote access to eval or property mutation in production.
2. **Agent-native.** JSON responses, predictable paths, no ceremony. An agent
   with `curl` or `requests` should be able to do useful work immediately.
3. **Main-thread-safe.** All Qt access goes through `run_on_main_sync`. No
   direct widget touching from the HTTP thread.
4. **Composable.** Each endpoint is a handler function. Apps can register custom
   endpoints for domain-specific debugging.

---

## 2. Architecture

### Transport: stdlib HTTP server in a thread

```python
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading

class DevtoolsServer:
    def __init__(self, port=8765):
        self.port = port
        self._server = None
        self._thread = None

    def start(self):
        self._server = HTTPServer(('127.0.0.1', self.port), DevtoolsHandler)
        self._thread = threading.Thread(target=self._server.serve_forever, daemon=True)
        self._thread.start()

    def stop(self):
        if self._server:
            self._server.shutdown()
            self._server = None
```

Every handler that touches Qt marshals via `run_on_main_sync`. The HTTP thread
blocks until the main thread executes the request and returns the result. For
a debug tool this latency is irrelevant.

### Handler pattern

```python
class DevtoolsHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        path = self.path
        if path == '/scene':
            result = run_on_main_sync(lambda: dump_scene_tree())
            self._json(200, result)
        elif path.startswith('/scene/'):
            name = path.split('/')[-1]
            result = run_on_main_sync(lambda: inspect_widget(name))
            self._json(200, result)
        elif path == '/logs':
            result = run_on_main_sync(lambda: tail_logs(100))
            self._json(200, result)
        else:
            self._json(404, {'error': 'not found'})

    def do_POST(self):
        # /eval, /scene/<name>/style, /scene/<name>/property
        ...

    def _json(self, code, body):
        import json
        data = json.dumps(body).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Content-Length', len(data))
        self.end_headers()
        self.wfile.write(data)
```

### Registration: apps can add endpoints

```python
DevtoolsServer.register_endpoint('/myapp/status', my_status_handler)
```

App-specific endpoints receive the parsed request body and return a JSON-serializable
dict. The server handles serialization and error wrapping.

---

## 3. Endpoints

### Scene tree

| Method | Path | Returns |
|--------|------|---------|
| GET | `/scene` | Full QObject tree as nested JSON (objectName, className, children, visibility) |
| GET | `/scene/<objectName>` | Single widget: properties, signals, state, geometry, stylesheet |
| GET | `/scene/<objectName>/children` | Direct children list |
| GET | `/scene/<objectName>/properties` | All readable properties (QMetaObject property dump) |

### Mutation

| Method | Path | Body | Effect |
|--------|------|------|--------|
| POST | `/scene/<objectName>/style` | `{"style": "..."}` | Set stylesheet on widget |
| POST | `/scene/<objectName>/property` | `{"name": "...", "value": ...}` | Set a Qt property |
| POST | `/scene/<objectName>/visible` | `{"visible": true/false}` | Show/hide widget |
| POST | `/scene/<objectName>/click` | `{}` | Simulate a click |

### Eval

| Method | Path | Body | Returns |
|--------|------|------|---------|
| POST | `/eval` | `{"code": "..."}` | Result of `eval(code)` in app namespace, or error |

Eval runs on the main thread via `run_on_main_sync`. The namespace includes
`QApplication.instance()`, `QApplication.topLevelWidgets()`, and any registered
globals. Dangerous — must be off by default.

### Logs

| Method | Path | Returns |
|--------|------|---------|
| GET | `/logs?limit=100` | Recent log records as JSON |
| GET | `/logs?level=ERROR` | Filtered logs |
| GET | `/logs/count` | Total record count |

### Settings

| Method | Path | Returns |
|--------|------|---------|
| GET | `/settings` | All QSettings keys/values |
| GET | `/settings/<key>` | Single setting |
| POST | `/settings/<key>` | Set a setting |

### App info

| Method | Path | Returns |
|--------|------|---------|
| GET | `/app` | App name, version, theme, process info, uptime |
| GET | `/app/widgets` | Flat list of all live widgets (objectName → className) |

---

## 4. Integration with BaseApplication

Two integration patterns, ordered by complexity:

### Phase 1: Explicit opt-in

```python
from qtstrap.extras.devtools import DevtoolsServer

app = BaseApplication(app_info=AppInfo)

devtools = DevtoolsServer(port=8765)
devtools.start()
```

No BaseApplication changes. Apps that want the debug port import and start it
themselves. Simplest, no risk to existing apps.

### Phase 2: Declarative flag (ties into async-guide §5)

```python
class Application(BaseApplication):
    DEVTOOLS = True  # or DEVTOOLS_PORT = 8765

app = Application()
app.run()  # devtools starts as part of run()
```

The flag enables the server during pre-init, alongside the CLI flag parser and
config resolution. The server shuts down in `aboutToQuit`.

### Security

- Bind to `127.0.0.1` only — no remote access.
- Optional `DEVTOOLS_TOKEN` env var or flag. If set, requests must include
  `Authorization: Bearer <token>`. If unset, no auth (localhost-only trust model).
- `/eval` requires explicit `DEVTOOLS_EVAL=True` — separate from the server
  enable flag. Defense in depth against accidental eval exposure.

---

## 5. Relationship to existing devtools

The existing in-app dock widgets (`SceneTreeDockWidget`, `StyleEditorDockWidget`,
`ReplDockWidget`) stay as-is — they're for humans. The HTTP server is a parallel
access path for agents, not a replacement.

Shared backend:
- `TreeNode.inverse` registry → used by both scene tree widget and `/scene` endpoint
- `inspect_widget()` logic → extracted from `Inspector.inspect()` into a reusable
  function returning a dict instead of setting QLabel text
- `tail_logs()` → queries the log database directly (same schema, different
  transport than `LogTableView`)

The inspector needs refactoring: currently it sets QLabel text directly. Extract
a `collect_widget_info(obj) -> dict` that both the inspector and the HTTP handler
call. The inspector formats the dict into labels; the HTTP handler serializes it
to JSON.

---

## 6. Open questions

- **WebSocket vs HTTP:** HTTP is simpler for agents (curl, requests). WebSocket
  gives push notifications for scene tree changes. Start with HTTP, add WS later
  if push is needed.
- **Scene tree change notifications:** the existing `TreeNode` uses
  `eventFilter` to detect child additions/removals. Could expose a
  `/scene/watch` SSE endpoint for live updates. Low priority.
- **REPL over HTTP:** `/eval` is the simple version. A persistent REPL session
  (maintaining namespace across calls) would need session management. Defer.
- **Style editor over HTTP:** `POST /scene/<name>/style` sets a stylesheet. The
  existing `StyleEditorDockWidget` uses Monaco for editing — that's a UI concern,
  not a backend one. The backend is just `widget.setStyleSheet(style)`.
- **Monaco dependency:** `style_editor.py` imports `monaco` which is a heavy
  dependency. The HTTP style endpoint doesn't need it. Consider making Monaco
  optional and falling back to a plain `QPlainTextEdit`.

---

## 7. Implementation order

1. **`run_on_main_sync`** (from new-utilities §1) — prerequisite. The HTTP server
   can't touch Qt without it.
2. **`collect_widget_info(obj) -> dict`** — extract from `Inspector`, reusable
   by both the inspector and HTTP handlers.
3. **`DevtoolsServer` + `/scene` + `/scene/<name>`** — minimal viable debug port.
   Prove the marshaling pattern works.
4. **`/eval`** — the killer feature for agents. Requires `DEVTOOLS_EVAL` flag.
5. **`/logs`** — query the existing log database.
6. **`/settings` + `/app`** — introspection endpoints.
7. **Mutation endpoints** (`/style`, `/property`, `/visible`, `/click`) — after
   the read side is solid.
8. **Declarative flag integration** — once the server is proven, wire it into
   `BaseApplication` as a flag.