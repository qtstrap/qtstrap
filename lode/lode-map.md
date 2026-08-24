---
type: domain
tags: [lode-map, navigation, routing]
keywords: [lode-map, navigation, routing, index, docs, qtstrap]
summary: Navigation index and entry point for the qtstrap lode documentation.
---

# Lode Map

qtstrap — Qt application bootstrapping framework (published on PyPI).

## Guides
- [async-guide.md](async-guide.md) - Async interop: why promises (not async/await) are the interface for qtstrap apps, the promisio/merged-loop design, `extras/promise` proposals with examples, and the BaseApplication packaging plan (declarative flags + `run()`). Includes design rationale — read before implementing any async-adjacent feature.
- [theming-guide.md](theming-guide.md) - Qt's four-layer theming model (QStyle/QPalette/QSS/paint-code), the rules for palette-based theming, and the `extras/style` v2 overhaul spec: semantic palette derivation, theme registry, theme-aware qcolors, themed icons, BaseApplication integration. Supersedes the detail of bugfix plan P2-16's style items.

## Plans
- [plans/bugfix-review-2026-07.md](plans/bugfix-review-2026-07.md) - Fixes for the July 2026 code review findings: portable mode, log monitor threading/SQL, PersistentCScrollArea, singleton, layout edge cases, plus an extras addendum (command palette regex crash, CommandRegistry QObject init, scene tree rescan, themes/settings_model). Ordered by severity with per-item edge cases and verification steps.
- [plans/devtools.md](plans/devtools.md) - Qt devtools system: fixing and refactoring existing in-app dock widgets (scene tree, inspector, style editor, REPL) into a shared backend, plus an agent-friendly HTTP debug control port. Status: idea.
- [plans/nodegraph.md](plans/nodegraph.md) - Fork and modernize NodeGraphQt as qtstrap.extras.nodegraph. Clean API, __init_subclass__ registration, theme awareness, chassis and command palette integration. Status: idea.
- [plans/application-chassis.md](plans/application-chassis.md) - VSCode-style window primitives extracted from Stagehand: Panel, Sidebar, ActivityBar, TabPanel, StatusBar, SettingsMenu. Panel/Sidebar/ActivityBar/StatusBar/TabPanel/Page implemented and tested (21 tests). StatusBar uses inner-container left/right zones, StatusBarItem auto-discovery with singleton support, side attribute, and get_item(). Remaining: DockRegistry, CommandRegistry, SystemTray, ShortcutManager. Status: active.
- [plans/command-palette.md](plans/command-palette.md) - Command palette thorough review: paint renderer issues, multi-stage option chaining, validation feedback, frecency cleanup, hardcoded colors. Status: idea.

## Notes
- **Packaging strategy — core + DLC:** qtstrap core stays lean (context layouts, persistent widgets, chassis slots, command palette, async runtime, theme registry). Heavy optional features are separate packages that depend on qtstrap but aren't part of it: `qtstrap-tabs` (split-tab system, if built), `qtstrap-nodegraph` (forked NodeGraphQt, 14K lines), `qtstrap-devtools` (HTTP control port). Each is `pip install`-able independently. An app only pays for what it imports. This matches continuous granularity at the package level — the core is the first level, each DLC adds more without imposing on the core.
 - **Context layout `__getattr__` shadowing:** `ContextLayout.__getattr__` proxies missing attributes to the stacked child (e.g. a `CScrollArea`). But `QLayout` methods like `widget()` and `count()` exist on the outer layout, so Python never calls `__getattr__` — `layout.scroll().widget()` returns `QLayout.widget()` (the parent widget), not `CScrollArea.widget()` (the inner content widget). This is a structural tradeoff of subclassing `QLayout` for the context-manager pattern, not a bug. The escape hatch is `layout._layout` to access the stacked child directly. Overriding individual methods on `CScrollArea`/`CSplitter` would be whack-a-mole. Documented, not patched.
 - **Gallery app (`gallery/main.py`):** Living example app exercising the full framework — chassis (Panel, Sidebar, ActivityBar, StatusBar with left/right items, TabPanel, Page), context layouts, persistent widgets, SettingsModel, command palette, awaitable dialog, async, CMenu context menus, theme switching. The reference implementation an agent should copy from.
 - **CMenu (`qtstrap.widgets.context_menu`):** Context-menu builder using context-manager stack pattern matching CVBoxLayout/CHBoxLayout. `menu.add(text, callback)`, `menu.submenu(title)` (nested `with`), `menu.sep()`, `menu += QAction`. Root `__exit__` calls `exec(event.globalPos())`; submenu `__exit__` calls `addMenu` on parent. Exported via `from qtstrap import *`.
 - **Agent eval methodology:** Run paired from-scratch app-building evals — one agent told to use qtstrap, one using raw Qt — then compare code size, feature adoption, and friction. The qtstrap agent's friction report is the primary discoverability signal. First eval (file browser): qtstrap agent produced 260 lines vs 352 raw (26% less), adopted BaseApplication, BaseMainWindow, PersistentCSplitter, SettingsModel, context layouts, chassis StatusBar. Found StatusBar.add_item() bug (now fixed), findChild workaround (now solved by get_item + singleton pattern), and missing left/right support (now added via side attribute).
