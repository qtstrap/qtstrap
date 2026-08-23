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
## Notes
- The two plans cross-reference each other: bugfix P2-10 (singleton rewrite) and P0-1 (portable mode) are prerequisites for the testing module (utilities §9); the debounce utility (§3) is referenced by bugfix P2-11d and P0-3.
- **Context layout `__getattr__` shadowing:** `ContextLayout.__getattr__` proxies missing attributes to the stacked child (e.g. a `CScrollArea`). But `QLayout` methods like `widget()` and `count()` exist on the outer layout, so Python never calls `__getattr__` — `layout.scroll().widget()` returns `QLayout.widget()` (the parent widget), not `CScrollArea.widget()` (the inner content widget). This is a structural tradeoff of subclassing `QLayout` for the context-manager pattern, not a bug. The escape hatch is `layout._layout` to access the stacked child directly. Overriding individual methods on `CScrollArea`/`CSplitter` would be whack-a-mole. Documented, not patched.
