---
type: plan
status: idea
tags: [plan, application-chassis, panels, sidebar, tabs, statusbar, extraction]
keywords: [application chassis, panel, sidebar, activity bar, tab system, status bar, settings menu, stagehand extraction, vscode layout]
summary: Extract Stagehand's working window chassis — activity bar, sidebar, tab system, status bar, settings menu — into qtstrap primitives so every app doesn't rebuild them.
---

# Plan: Application Chassis

## Context

Every Qt desktop app needs the same window infrastructure: a panel/dock
management system, a sidebar with activity bar, a tab system, a status bar,
a settings menu, and a command palette registration point. Qt gives you
`QMainWindow` and says good luck.

Stagehand has a working first implementation of all of these, built on top
of qtstrap's `BaseMainWindow` and `BaseDockWidget`. The pieces are tested in
production use but entangled with Stagehand-specific concerns (OBS plugins,
device controls, uinput). This plan extracts the reusable chassis into
qtstrap.

Related: [devtools.md](devtools.md) (devtools docks use the same chassis),
[new-utilities.md](new-utilities.md) §1 (`run_on_main` — chassis registration
may need main-thread guards for plugin loading).

---

## 1. What Stagehand has

### Activity bar + sidebar (`components.py`, `main_window.py`)

- `StagehandSidebar` — base class with `name`, `display_name`, `icon_name`.
  Discovery via `__subclasses__()`.
- `SidebarContainer` — `QStackedWidget` that auto-discovers and instantiates
  all sidebar subclasses. Toggle visibility, switch panels by name.
- `create_activity_bar()` — left-side `BaseToolbar` with one icon button per
  discovered panel, toggles the sidebar on click.

### Tab system (`tabs.py`)

- `MainTabWidget` — persistent tabs with drag reorder (`TabBar` subclass),
  context menu (rename, remove, add), save/load to JSON, page registration via
  subclass discovery (`StagehandPage.get_subclasses()`).
- `StagehandPage` — base class with `get_name()`, `label` (LabelEdit for
  rename), serialization hooks (`serialize()` / `deserialize()`).

### Status bar (`main_window.py`)

- `create_statusbar()` — `BaseToolbar` at the bottom with a gear button,
  settings menu, and status bar items.
- `init_statusbar_items()` — registers app-specific status widgets.

### Settings menu (`main_window.py`)

- `init_settings_menu()` — adds standard items (theme, font, about, exit)
  plus app-specific items.

### Dock management (`main_window.py`)

- `BaseDockWidget` subclasses for log monitor, (commented out) devtools,
  device controls. Each declares `_title`, `_starting_area`, `_shortcut`.

### System tray (`main_window.py`)

- Tray icon, minimize-to-tray action, update notifications.

---

## 2. Extraction targets

### `Panel` base class

```python
class Panel(QWidget):
    """Base class for sidebar panels. Subclasses define:
        name: unique identifier (used for lookup)
        display_name: human-readable name (shown in tooltip)
        icon_name: qtawesome icon name (shown in activity bar)
    Registration is automatic via __init_subclass__ — subclassing Panel is
    the registration. No decorator, no manifest, no __subclasses__() walk.
    """
    _registry: dict[str, type['Panel']] = {}

    name = ''
    display_name = ''
    icon_name = ''

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not getattr(cls, 'name', ''):
            raise TypeError(f'{cls.__name__} must define a name')
        if cls.name in Panel._registry:
            raise TypeError(f'{cls.__name__} duplicates panel name {cls.name!r}')
        Panel._registry[cls.name] = cls
```

Replaces `StagehandSidebar`. Registration is automatic, validated, and
deduplicated at class definition time. Import errors (missing `name`,
duplicate names) surface immediately instead of at runtime when the sidebar
tries to instantiate a panel and gets a confusing failure.

### `Sidebar` container

```python
class Sidebar(QWidget):
    """Manages all sidebar panels in a QStackedWidget.
    Reads from Panel._registry. Toggle via activity bar.
    Persists which panel is visible and whether sidebar is shown.
    """
    def __init__(self, parent=None): ...
    def show_panel(self, name: str): ...
    def toggle_panel(self, name: str) -> bool: ...
    def register_panel(self, panel: type[Panel]): ...  # explicit registration
```

Replaces `SidebarContainer`. Reads from `Panel._registry` instead of
`__subclasses__()`. Explicit `register_panel()` available for apps that
need dynamic registration (e.g. plugin loading at runtime).

### `ActivityBar`

```python
class ActivityBar(BaseToolbar):
    """Left-side icon strip. Auto-populates from Sidebar's registered panels.
    Click toggles the corresponding sidebar panel.
    """
    def __init__(self, parent, sidebar: Sidebar): ...
```

Replaces `create_activity_bar()`. No more manual button creation in
`MainWindow.__init__`.

### `TabBar` / `TabSystem`

```python
class Page(QWidget):
    """Base class for tab pages with serialization.
    Registration is automatic via __init_subclass__.
    """
    _registry: dict[str, type['Page']] = {}

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not getattr(cls, 'page_type', ''):
            raise TypeError(f'{cls.__name__} must define a page_type')
        if cls.page_type in Page._registry:
            raise TypeError(f'{cls.__name__} duplicates page type {cls.page_type!r}')
        Page._registry[cls.page_type] = cls

    page_type = ''
    def get_name(self) -> str: ...
    def serialize(self) -> dict: ...
    def deserialize(self, data: dict): ...

class TabSystem(QTabWidget):
    """Persistent tabs with drag reorder, context menu, save/load.
    Reads from Page._registry.
    """
    def create_page(self, page_type: str = None): ...
    def add(self, page: Page): ...
    def save(self): ...
    def load(self): ...
```

Replaces `MainTabWidget` + `TabBar` + `StagehandPage`. The drag/reorder,
context menu, and save/load logic is Stagehand-agnostic — it operates on
the `Page` interface, not on Stagehand's action system.

### Split panels: explicitly out of scope

VSCode-style split editor areas (drag tabs between splits, drop-to-split
overlays, nested splitters, tear-off floating windows) are NOT in the chassis.
The interaction edges — drag thresholds, drop target highlighting, tab
tear-off vs reorder, empty split cleanup, focus management, resize during
drag, keyboard navigation, platform-specific DnD semantics — are each small
in code but enormous in edge cases. A quarter-polished implementation would
feel broken where it matters most.

Worse, a split manager that owns the interaction edges would impose
constraints on tab contents — wrapping or intercepting them for focus and
drag management. That violates the chassis principle: the content owns
itself, the framework provides a slot.

The chassis `TabSystem` provides single-tab-bar persistence and reorder.
Apps that need VSCode-style splitting build their own split manager and wire
it into the `TabSystem` slot, or bring a docking engine (KDDockWidgets,
Qt-Advanced-Docking-System). qtstrap provides the registration system and
the slot; the split interaction is the app's problem to own or delegate.

### `StatusBar`

```python
class StatusBar(BaseToolbar):
    """Status bar with settings menu and registered items."""
    def __init__(self, parent): ...
    def add_item(self, widget: QWidget): ...
    def add_settings_action(self, text: str, callback): ...
```

Replaces `create_statusbar()` + `init_statusbar_items()`. Standard items
(theme, font, about, exit) are added automatically; apps register custom
items via `add_item()`.

### `SettingsMenu`

```python
class SettingsMenu(QMenu):
    """Standard settings menu with theme, font, about, exit.
    Apps add custom actions via add_action().
    """
    def __init__(self, parent=None): ...
    def add_action(self, text: str, callback, shortcut=None): ...
```

Replaces `init_settings_menu()`. The standard items are built in; app-specific
items are additive.

### `DockRegistry`

```python
class DockRegistry:
    """Central registry for dock widgets.
    Docks register via __init_subclass__ on BaseDockWidget or explicit registration.
    MainWindow can auto-instantiate all registered docks.
    """
    def register(self, dock: type[BaseDockWidget]): ...
    def instantiate_all(self, parent: QMainWindow) -> dict[str, BaseDockWidget]: ...
```

Replaces manual `self.log_monitor = LogMonitorDockWidget(self)` in
`MainWindow.__init__`. Docks that need deferred instantiation or conditional
visibility can be registered with a factory.

### `CommandRegistry`

```python
class CommandRegistry:
    """Central registry for command palette commands.
    Any object can register commands. The command palette reads from here.
    """
    def register(self, command: Command): ...
    def register_all(self, obj: QObject): ...  # reads obj.commands attribute
    def get_commands(self) -> list[Command]: ...
```

Replaces the scattered `self.commands = [Command(...)]` pattern. Each chassis
component (panels, docks, pages) can register its own commands via
`register_all(self)` and they all appear in the command palette automatically.

### `SystemTray`

```python
class SystemTray(QObject):
    """System tray icon with minimize-to-tray and notification support.
    """
    def __init__(self, parent, icon=None): ...
    def set_menu(self, actions: list): ...
    def notify(self, title: str, message: str): ...
    def set_minimize_to_tray(self, enabled: bool): ...
```

Replaces the hand-rolled tray setup in `MainWindow.__init__`. The minimize-to-
tray behavior uses a `PersistentCheckableAction` for its toggle.

### `ShortcutManager`

```python
class ShortcutManager:
    """Registers and manages QShortcuts on a widget.
    Shortcuts can be registered by name and looked up later.
    """
    def register(self, name: str, sequence: str, callback, widget=None): ...
    def get(self, name: str) -> QShortcut: ...
    def register_tab_shortcuts(self, tab_system, count=10): ...
```

Replaces the manual `for i in range(10): QShortcut(...)` loop. Standard
shortcut sets (tab switching, panel toggling) are built-in helpers.

## 3. Composition

The goal: a `MainWindow` that assembles the chassis from primitives instead
of building each piece by hand.

### Before (Stagehand today)

```python
class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.font_menu = FontSizeMenu(self)
        self.theme_menu = ThemeMenu(self)
        self.log_monitor = LogMonitorDockWidget(self)
        self.command_palette = CommandPalette(self)
        self.tabs = MainTabWidget()
        self.sidebar = SidebarContainer(self)
        self.create_activity_bar()
        self.create_statusbar()
        self.init_statusbar_items()
        self.init_settings_menu()
        self.init_tray_stuff()
        # ... 60 more lines of wiring
```

### After (with chassis primitives)

```python
class MainWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        
        self.sidebar = Sidebar(self)
        self.activity_bar = ActivityBar(self, self.sidebar)
        self.tabs = TabSystem(self)
        self.status_bar = StatusBar(self)
        self.settings_menu = self.status_bar.settings_menu
        
        self.log_monitor = LogMonitorDockWidget(self)
        self.command_palette = CommandPalette(self)
        
        # Register custom items
        self.status_bar.add_item(MyStatusWidget())
        self.settings_menu.add_action('Check for Updates', self.check_updates)
```

The chassis handles discovery, wiring, persistence, and standard items.
The app code declares what it needs, not how to build it.

---

## 4. What stays app-specific

- **Panel contents** — each panel's widgets and logic are the app's business
- **Page types** — `ActionsPage`, `GodotPage`, etc. are Stagehand-specific
- **Dock contents** — `LogMonitorDockWidget` is qtstrap; `DeviceControlsDockWidget`
  is Stagehand
- **Status bar items** — OBS status, Godot status, etc. are Stagehand-specific
- **Settings menu items** — uinput setup, app updater are Stagehand-specific
- **Tray behavior** — minimize-to-tray policy is app-specific
- **Command palette commands** — app-specific registrations

The chassis provides the *slots*. The app fills them.

### The contribution IS the widget

Inspired by Stagehand's `StagehandStatusBarItem(QWidget): pass` — the only
requirement for contributing a status bar item is "be a QWidget subclass of
the marker class." No JSON manifest, no callback registration, no data
structure the framework interprets. You write a QWidget, it shows up.

Every chassis component follows this principle:
- **StatusBar** — subclass the marker, your widget appears in the status bar
- **Panel** — subclass `Panel`, your widget appears in the sidebar
- **Page** — subclass `Page`, your widget appears in the tab system
- **Dock** — subclass `BaseDockWidget`, your widget appears as a dock

This is a deliberate rebellion against the VSCode extension API, where the
framework owns the entire presentation layer and contributions are data
structures or narrow callback handlers. qtstrap chassis is the opposite: the
widget is the contribution, the framework provides the slot.

### Required vs. optional

Required attributes are enforced at class definition time via
`__init_subclass__` (missing `name`, missing `page_type`, duplicates). These
are the minimal requirements for the chassis to do its job — a panel needs
a name so the sidebar can address it, a page needs a type so the tab system
can save/load it.

Everything else is optional and degrades gracefully:
- `icon_name` missing → Panel shows with a default icon
- `display_name` missing → Panel uses `name` as display name
- `serialize()` missing → Page can't be persisted, works for the session
- `_shortcut` missing → Dock has no keyboard shortcut
- No `Panel` subclasses → Sidebar is empty, no error
- No `StatusBarItem` subclasses → StatusBar has just the standard items
- No `Page` subclasses → TabSystem starts with no tabs

The rule: helper features MUST be optional and degrade gracefully. A missing
attribute or method never crashes the chassis — it just means that feature
isn't available for that contribution.

### Continuous granularity

Each chassis piece is usable independently. Composing more of them gives you
more, but no piece requires another to function:

- `Panel` + `Sidebar` without `ActivityBar` — sidebar with manual switching
- `StatusBar` without `Sidebar` — just a status bar with settings menu
- `TabSystem` with plain `QWidget`s — tabs without the `Page` registration system
- `CommandRegistry` without any other chassis piece — just a command palette

This is the same principle as qtstrap's context layouts: `CVBoxLayout` doesn't
require `CFormLayout`. Each piece stands alone.

The mechanism: interfaces, not inheritance. `TabSystem` accepts any `QWidget`
that has `serialize()`/`deserialize()`, not only `Page` subclasses. `ActivityBar`
works with any object exposing `toggle_panel(name)`, not only the qtstrap
`Sidebar`. No piece forces another into your app.
---

## 5. Implementation order

1. **`Panel` + `Sidebar`** — extract from `SidebarContainer`. Panel uses
   `__init_subclass__` for automatic, validated registration (replaces
   `__subclasses__()` walk). Test with a minimal panel.
2. **`ActivityBar`** — extract from `create_activity_bar()`. Auto-populate
   from `Sidebar`.
3. **`StatusBar` + `SettingsMenu`** — extract from `create_statusbar()` and
   `init_settings_menu()`. Standard items built in.
4. **`Page` + `TabSystem`** — extract from `MainTabWidget` + `StagehandPage`.
   Page uses `__init_subclass__` for registration (replaces
   `get_subclasses()` walk). Generalize the save/load format.
5. **`DockRegistry`** — central dock registration, auto-instantiation.
6. **`CommandRegistry`** — central command registration, auto-collection
   from chassis components.
7. **`SystemTray`** — tray icon, minimize-to-tray, notifications.
8. **`ShortcutManager`** — shortcut registration, standard shortcut sets.
9. **Integration test** — build a minimal app using all chassis primitives,
   verify it works without Stagehand-specific code.
10. **Migrate Stagehand** — replace `SidebarContainer`, `create_activity_bar()`,
   `MainTabWidget`, `create_statusbar()`, manual dock wiring, manual shortcut
   loops, `self.commands` lists with chassis primitives. Verify nothing breaks.
11. **Documentation** — example app showing the chassis in use.