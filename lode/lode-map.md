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
- [plans/new-utilities.md](plans/new-utilities.md) - Nine proposed additions: main-thread marshaling, background workers, debounce/throttle, updater (upstreamed from Stagehand), single-instance guard, crash dialog, block_signals, toasts, and a pytest testing module. Ordered by evidence of need; §1–3 are the "concurrency kit".

## Notes
- The two plans cross-reference each other: bugfix P2-10 (singleton rewrite) and P0-1 (portable mode) are prerequisites for the testing module (utilities §9); the debounce utility (§3) is referenced by bugfix P2-11d and P0-3.
