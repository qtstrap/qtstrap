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
    Discovery is automatic via __subclasses__().
    """
    name = ''
    display_name = ''
    icon_name = ''
```

Replaces `StagehandSidebar`. No behavioral change — just renamed and moved.

### `Sidebar` container

```python
class Sidebar(QWidget):
    """Manages all sidebar panels in a QStackedWidget.
    Auto-discovers Panel subclasses. Toggle via activity bar.
    Persists which panel is visible and whether sidebar is shown.
    """
    def __init__(self, parent=None): ...
    def show_panel(self, name: str): ...
    def toggle_panel(self, name: str) -> bool: ...
    def register_panel(self, panel: type[Panel]): ...  # explicit registration
```

Replaces `SidebarContainer`. Adds explicit `register_panel()` for apps that
don't want to rely on `__subclasses__()` discovery.

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
    """Base class for tab pages with serialization."""
    def get_name(self) -> str: ...
    def serialize(self) -> dict: ...
    def deserialize(self, data: dict): ...

class TabSystem(QTabWidget):
    """Persistent tabs with drag reorder, context menu, save/load.
    Pages register via subclass discovery or explicit registration.
    """
    def create_page(self, page_type: str = None): ...
    def add(self, page: Page): ...
    def save(self): ...
    def load(self): ...
```

Replaces `MainTabWidget` + `TabBar` + `StagehandPage`. The drag/reorder,
context menu, and save/load logic is Stagehand-agnostic — it operates on
the `Page` interface, not on Stagehand's action system.

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

---

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

---

## 5. Implementation order

1. **`Panel` + `Sidebar`** — extract from `SidebarContainer`, add explicit
   registration. Test with a minimal panel.
2. **`ActivityBar`** — extract from `create_activity_bar()`. Auto-populate
   from `Sidebar`.
3. **`StatusBar` + `SettingsMenu`** — extract from `create_statusbar()` and
   `init_settings_menu()`. Standard items built in.
4. **`Page` + `TabSystem`** — extract from `MainTabWidget` + `StagehandPage`.
   Generalize the save/load format.
5. **Integration test** — build a minimal app using all chassis primitives,
   verify it works without Stagehand-specific code.
6. **Migrate Stagehand** — replace `SidebarContainer`, `create_activity_bar()`,
   `MainTabWidget`, `create_statusbar()` with chassis primitives. Verify
   nothing breaks.
7. **Documentation** — example app showing the chassis in use.