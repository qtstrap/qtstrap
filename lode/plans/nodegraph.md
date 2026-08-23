---
type: plan
status: idea
tags: [plan, nodegraph, node-graph, dataflow, graphics, fork, NodeGraphQt]
keywords: [nodegraph, node graph, dataflow, QGraphicsScene, NodeGraphQt, fork, visual programming, qtstrap extras]
summary: Fork and modernize NodeGraphQt as qtstrap.extras.nodegraph — clean up the API, integrate with the chassis and theme system, add qtstrap conventions.
---

# Plan: Node Graph

## Context

There is no good node graph library in the Python/Qt ecosystem. The biggest
is [NodeGraphQt](https://github.com/jchanvfx/NodeGraphQt) by jchanvfx — used
in Nuke-style compositing tools, shader editors, and pipeline tools. It's
ancient, stuck at v0.6.18 "Work in Progress," the API is rough, and upstream
is effectively dead.

Stagehand vendors a copy at
`Stagehand/src/stagehand/plugins/nodegraph/packages/NodeGraphQt/` (14.6K lines).
It's already migrated to `qtpy` (works with PySide6). The graphics code — the
hard part — works fine. The "disgusting" parts are the API surface: node
registration, property widgets, the model/view split, the import structure.

This plan: fork NodeGraphQt into `qtstrap.extras.nodegraph`, clean up the API
to match qtstrap conventions, and integrate with the chassis and theme system.

Related: [application-chassis.md](application-chassis.md) (node graph as a
panel/page type, command palette integration), [devtools.md](devtools.md)
(scene tree inspection of graph nodes).

---

## 1. Current state of NodeGraphQt

### Architecture

```
NodeGraphQt/
├── base/
│   ├── graph.py      2997 lines — NodeGraph controller, registration, serialization
│   ├── node.py        528 lines — NodeObject base class
│   ├── port.py               — Port class
│   ├── model.py      622 lines — NodeModel, PortModel, NodeGraphModel (serialization)
│   ├── commands.py          — QUndoCommand subclasses (move, connect, delete)
│   ├── factory.py           — NodeFactory (registration lookup)
│   └── menu.py              — context menu system
├── qgraphics/              — QGraphicsScene/QGraphicsItem rendering (the hard part)
│   ├── node_base.py  1045 lines — node item rendering, ports, layout
│   ├── port.py              — port item (circle, drag-to-connect)
│   ├── pipe.py              — bezier connection rendering
│   ├── slicer.py            — connection slicing (alt-drag to cut)
│   └── node_*.py           — node variants (circle, backdrop, group)
├── widgets/
│   ├── viewer.py     1624 lines — NodeViewer (QGraphicsView, zoom, pan, selection)
│   ├── node_graph.py        — NodeGraphWidget (main widget)
│   └── viewer_nav.py        — navigation/zoom widget
├── custom_widgets/
│   ├── nodes_tree.py        — node tree for the "add node" panel
│   ├── nodes_palette.py     — node palette (drag to add)
│   └── properties_bin/      — property editor panel with widget types
├── nodes/
│   ├── base_node.py         — BaseNode (adds ports, properties to NodeObject)
│   ├── backdrop_node.py    — backdrop (grouping container)
│   ├── group_node.py        — group node (subgraph)
│   └── ...
├── constants.py            — enums, colors, sizes
└── errors.py
```

### What works

- **Graphics:** `QGraphicsScene`/`QGraphicsView` with zoom, pan, rubber band
  selection, port drag-to-connect, bezier connections, connection slicing,
  backdrops, group nodes. This is thousands of hours of work that works.
- **Undo/redo:** full `QUndoStack` with move, connect, disconnect, delete,
  property change commands.
- **Serialization:** `serialize()`/`deserialize()` to JSON. Node positions,
  connections, properties, IDs all saved/restored.
- **qtpy compatibility:** already imports from `qtpy`, not PySide2 directly.

### What's ugly

1. **Node registration:** `graph.register_node(cls)` + `graph.create_node('io.github.jchanvfx.MyNode')`.
   Nodes identified by `__identifier__` + class name string. No
   `__init_subclass__`, no validation, no deduplication. The identifier scheme
   is a Java-style reverse-DNS that nobody remembers to change.

2. **Import structure:** `from NodeGraphQt import NodeGraph, BaseNode`. Absolute
   imports, not relative. Breaks if the package is renamed or moved. The
   `__init__.py` says PySide2 despite being qtpy.

3. **Model/view split:** `NodeObject` (logic) ↔ `NodeModel` (data) ↔
   `QGraphicsItem` (view). Three objects per node. The model is a plain class
   with `__dict__` serialization — no validation, no types.

4. **Property widgets:** `NodePropWidgetEnum` maps property types to widget
   types. Custom property widgets are registered through a factory with string
   keys. No integration with qtstrap's persistent widgets or SettingsModel.

5. **Context menu from JSON:** `graph.set_context_menu_from_file('hotkeys.json')`.
   A JSON file defines the right-click menu. Over-engineered and fragile.

6. **Signal spam:** the Stagehand integration connects 12 separate signals
   just to know "something changed." No aggregated `graph_changed` signal.

7. **`_viewer` access:** `graph._viewer.moved_nodes.connect(...)` — reaching
   into private attributes to wire up change notifications.

8. **No theme awareness:** colors are hardcoded in `constants.py` and
   per-node `color=` kwargs. No palette integration, no theme switching.

9. **Documentation in docstrings:** every class has 20+ lines of Sphinx
   formatting in its docstring. Readable but heavy.

---

## 2. Fork strategy

### Fork, don't vendor

Create a proper fork: `qtstrap.extras.nodegraph`. The package lives in
qtstrap's source tree, not as a vendored copy. This means:

- Relative imports throughout (`from .base.graph import NodeGraph`)
- Package name is `qtstrap.extras.nodegraph`
- No `NodeGraphQt` references in import paths
- The fork can diverge from upstream freely — upstream is dead

### What to keep unchanged

- **All `qgraphics/` code** — the rendering layer works. Don't touch it
  unless a theme integration requires it.
- **`base/commands.py`** — the undo/redo commands work.
- **`widgets/viewer.py`** — the `NodeViewer` works.
- **`base/model.py`** — the serialization format works. Don't break it.

### What to clean up

1. **Imports:** convert all `from NodeGraphQt...` to `from .` (relative).
   One pass with a script.

2. **Node registration:** replace `__identifier__` + `register_node()` with
   `__init_subclass__` on `BaseNode`:
   ```python
   class BaseNode(NodeObject):
+      _registry: dict[str, type['BaseNode']] = {}
+
+      node_type = ''  # replaces __identifier__ + class name
+
+      def __init_subclass__(cls, **kwargs):
+          super().__init_subclass__(**kwargs)
+          if not getattr(cls, 'node_type', ''):
+              raise TypeError(f'{cls.__name__} must define a node_type')
+          if cls.node_type in BaseNode._registry:
+              raise TypeError(f'{cls.__name__} duplicates node type {cls.node_type!r}')
+          BaseNode._registry[cls.node_type] = cls
   ```
   `graph.create_node('nodes.basic.MyNode')` → `graph.create_node('nodes.basic.MyNode')`
   (same string, but now it comes from the registry, not the factory). Or
   simplify to `graph.create_node(MyNode)` — pass the class, not a string.

3. **Aggregated change signal:** add a single `graph_changed = Signal()`
   that fires on any modification (node added, removed, moved, connected,
   disconnected, property changed). The 12 individual signals stay for
   fine-grained use, but `graph_changed` is what 90% of consumers want.

4. **Property widgets → qtstrap integration:** map NodeGraphQt property
   types to qtstrap persistent widgets. `PropWidgetEnum.QLINE_EDIT` →
   `PersistentLineEdit`, `CHECKBOX` → `PersistentCheckBox`, `COMBO_BOX` →
   `PersistentComboBox`. Optional: support `SettingsModel` fields as node
   properties via the `model=` kwarg.

5. **Context menu:** remove the JSON file system. Context menus built
   programmatically with the chassis `CommandRegistry`.

6. **Theme awareness:** read colors from `QApplication.palette()` instead
   of `constants.py` hex values. Node background, port colors, connection
   colors, selection highlight — all from the palette. Exotic themes
   (vscode-dark) can style the graph via QSS on `NodeGraphWidget` class names.

7. **Docstrings:** strip Sphinx formatting, keep concise. The API docs
   should live in qtstrap's mkdocs, not in docstrings.

---

## 3. Integration with qtstrap

### As a chassis panel/page

```python
class NodeGraphPanel(Panel):
    name = 'nodegraph'
    display_name = 'Node Graph'
    icon_name = 'mdi.graph'

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.graph = NodeGraph()
        # auto-registers all BaseNode subclasses
        with CVBoxLayout(self, margins=0) as layout:
            layout.add(self.graph.widget)
```

### Node library as command palette

```python
# "Add Node: Math/Add" appears in the command palette
for node_type, cls in BaseNode._registry.items():
    CommandRegistry.register(
        Command(f'Add Node: {node_type}', triggered=lambda c=cls: graph.create_node(c))
    )
```

### Property panel

The `PropertiesBinWidget` becomes a qtstrap widget that uses the chassis
inspector pattern — select a node, see its properties in a side panel.
With SettingsModel integration, node properties can be typed and validated.

### Devtools integration

The devtools `/scene` endpoint walks the QGraphicsScene, not just QWidget
children. A node graph is a scene, not a widget tree — but the inspector
pattern is the same: `collect_node_info(node) -> dict`.

---

## 4. What this is NOT

- **Not an execution engine.** The graph is a visual editor for connections
  and properties. How the graph *runs* (topological sort, lazy evaluation,
  event-driven) is the app's concern, not qtstrap's. NodeGraphQt doesn't
  execute graphs either — it's purely the editor.
- **Not a replacement for the chassis.** The node graph is an extra, not a
  chassis component. Apps that don't need it don't import it.
- **Not a from-scratch rewrite.** The graphics code stays. The cleanup is
  API surface, imports, registration, and integration — not rendering.

---

## 5. Implementation order

1. **Fork:** copy `NodeGraphQt/` into `src/qtstrap/extras/nodegraph/`. Fix
   all imports to relative. Verify it imports and the Stagehand nodegraph
   page works against the new location.
2. **Node registration:** replace `__identifier__` + `register_node()` with
   `__init_subclass__` on `BaseNode`. Update `graph.create_node()`.
3. **Aggregated `graph_changed` signal:** fire on any modification. Update
   Stagehand to use it instead of 12 individual connections.
4. **Theme awareness:** replace `constants.py` color lookups with palette
   reads. Test with light/dark theme switching.
5. **Property widgets:** map to qtstrap persistent widgets. Optional
   SettingsModel integration.
6. **Context menu:** replace JSON file system with programmatic menus.
7. **Command palette integration:** register node types as commands.
8. **Chassis integration:** `NodeGraphPanel`, property panel as inspector.
9. **Devtools integration:** `/scene` endpoint for graph inspection.
10. **Tests:** smoke test graph creation, node registration, serialization
    round-trip, connection/disconnection.
11. **Documentation:** node graph guide showing how to define nodes, build
    a graph, and integrate with the chassis.