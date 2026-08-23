---
type: domain
tags: [guide, theming, qpalette, qss, style]
keywords: [qt, styling, theme, palette, fusion, qss, stylesheet, dark, light, theming, qtstrap]
summary: A deep guide to Qt's layered theming mechanisms and the qtstrap theme system overhaul spec.
---

# Theming Guide: How Qt Styling Actually Works, and the qtstrap Theme System Overhaul

Qt theming is confusing because Qt has **four theming mechanisms stacked on top of
each other**, with undocumented precedence rules and bad failure modes when mixed.
This guide gives the layer model first (the mental model that makes everything
else predictable), then diagnoses the current state of `extras/style`, then specs
the overhaul. Like the async guide, the rationale is included on purpose — do not
"simplify" the design without understanding why a rule exists.

Related: [plans/bugfix-review-2026-07.md](plans/bugfix-review-2026-07.md) P2-16
(style small fixes — superseded in detail by §4 here),
[async-guide.md](async-guide.md) §5 (BaseApplication packaging — theming hooks in).

---

## 1. The four-layer model

### Layer 1: QStyle — the drawing engine

`fusion`, `windowsvista`, `macos`, etc. The style decides *how* widgets are
painted: shapes, gradients, metrics, animation. Two facts drive everything:

1. **Native styles largely ignore QPalette.** `windowsvista` and `macos` delegate
   drawing to the OS theme engine, which uses OS colors regardless of what
   palette you set. A dark QPalette on `windowsvista` produces broken half-light
   widgets — some elements follow the palette, most don't.
2. **Fusion is the only style that fully respects the palette on every
   platform.** This is why "dark theme = Fusion + dark palette" is the universal
   Qt recipe, and why any serious theme system standardizes on Fusion.

Also: `windowsvista` simply doesn't exist off Windows —
`QApplication.setStyle('windowsvista')` returns None silently and the app keeps
whatever style it had.

### Layer 2: QPalette — the color inputs the style reads

Only meaningful to the extent Layer 1 consults it. The roles that do 90% of the
work:

| Role pair | What it colors |
|---|---|
| `Window` / `WindowText` | containers, labels, most chrome |
| `Base` / `Text` | input fields, item views, text editors |
| `Button` / `ButtonText` | buttons and button-likes |
| `Highlight` / `HighlightedText` | selections everywhere |
| `AlternateBase` | zebra striping in views |
| `ToolTipBase` / `ToolTipText` | tooltips |
| `Link` / `LinkVisited` | rich-text links |
| `Disabled` group of all of the above | disabled widgets |
| `Light`/`Midlight`/`Mid`/`Dark`/`Shadow` | 3D bevels — Fusion derives frames from these |

Traps:

- **Widget-level `setPalette` breaks inheritance permanently.** Setting a palette
  on an individual widget sets an internal flag (`WA_SetPalette`) that stops it
  inheriting the application palette forever after — the source of every "one
  widget stayed light after the theme switch" bug. Rule: only
  `QApplication.setPalette` for theming; widget-level palettes are for
  deliberate, permanent exceptions.
- **Order matters: `setStyle` BEFORE `setPalette`.** Setting the style can reset
  the application palette to the style's `standardPalette()`. The current
  `apply_theme` does palette-then-style — swap it (see §4.2).
- Live palette changes propagate automatically (widgets receive
  `QEvent.ApplicationPaletteChange`), but widgets that *cache* colors (custom
  paint code, pixmap caches) must handle that event and re-resolve.

### Layer 3: Stylesheets (QSS)

The one that burns everyone: **QSS is not an override of the style — it is a
replacement.** Setting almost any QSS property on a widget silently swaps its
rendering to `QStyleSheetStyle`, which discards Fusion/native drawing for the
affected elements and half-detaches the widget from the palette. Symptoms:
widgets that ignore theme switches, hover states that vanish, focus rings that
look alien.

Rules:

- Pick palette-based **or** QSS-based theming per application and be a zealot.
  qtstrap apps are palette-based.
- Per-widget QSS band-aids are forbidden in palette-themed apps. (The
  command palette's commented-out QLineEdit stylesheet was this rule being
  learned.)
- The one sanctioned QSS use: an optional *theme-level* stylesheet applied
  app-wide as part of a theme definition (§4.3), for the few things palettes
  can't express (e.g. flat scrollbars). Even then, prefer not.
- For **state-driven** styling (error borders, active highlights), use the
  dynamic-property pattern, which composes with palette theming:

  ```python
  widget.setProperty('status', 'error')
  widget.style().unpolish(widget)
  widget.style().polish(widget)
  ```
  with a theme-level QSS rule `QLineEdit[status="error"] { border: 1px solid ...; }`.
  This is the only pattern where per-selector QSS is acceptable, because it lives
  in the theme definition, not scattered on widgets.

### Layer 4: colors in paint code

Custom delegates and widgets are invisible to all three layers above. Rules:

- Paint code pulls colors from `option.palette` (delegates) or `self.palette()`
  (widgets) **at paint time** — never cached in `__init__`, never hex literals.
- Colors the palette genuinely lacks (success green, warning amber, an accent
  cyan) come from the semantic color vocabulary (§4.4) — the *only* legal source
  of non-palette color in paint code — and are re-read on theme change.

Current violations, all found in review: `PopupDelegate.get_colors` hardcodes
selected-white and cyan (bugfix plan P2-14); `SceneTreeWidgetItem` sets
`qcolors.white` foreground — **invisible text on the light theme**; qtawesome
icons created with literal colors (`qta.icon('fa.gear', color='gray')`).

### Special case: qtawesome icons

`qta.icon(name, color=...)` **bakes the color at call time**. `qta.reset_cache()`
alone cannot fix icons already handed to widgets — they hold rendered pixmaps.
Theme switching therefore requires icon *consumers* to re-create their icons.
This is the `TODO: find and redraw all icons` in `base_application.py`, and §4.5
is the fix.

---

## 2. Diagnosis of the current system

`extras/style/` today: `themes.py` (dark/light palette factories + `apply_theme`),
`dark_palette.py` (a second, unused? dark palette), `colors.py` (`qcolors`
constants). Problems, in rough severity order:

1. Light theme uses `windowsvista` — wrong mechanism (Layer 1 fact #1), and
   nonexistent off Windows. Both themes must be Fusion.
2. `apply_theme` calls `unpolish` and never `polish`, and applies palette before
   style (reset hazard).
3. No registry — `_themes` is a closed dict, `ThemeMenu` in `base_window.py`
   hardcodes exactly Light/Dark actions. Apps with their own palette (DeviceManager)
   cannot join the system, so they bypass it entirely. **DeviceManager hand-rolls
   `setStyle('Fusion')` + its own `darkPalette` + its own icon color — the
   clearest evidence the system needs the overhaul.**
4. Palettes are hand-set role-by-role (~25 lines per theme) — hard to write, hard
   to keep consistent, high barrier for new themes.
5. `qcolors` is a static constant set, not theme-aware; devtools uses it in ways
   that break on light theme.
6. Icon refresh unsolved (the base_application TODO).
7. `OPTIONS.theme` integration incomplete (the file's own TODO): theme name
   validation, persistence, and the changed signal all live in
   `BaseApplication.change_theme` with no registry to consult.

---

## 3. The rules (project conventions)

### Design direction: themes as examples, not an imposed system

qtstrap does not impose theming. Apps that want native Qt appearance should
not have to fight a framework-level theme. The theme system provides:

- Two standard built-in themes (light, dark) for apps that want sensible
  defaults without writing their own.
- Example "exotic" themes (vscode-dark, flat-material) that demonstrate QSS
  presentation — not just colors but the whole visual language: flat buttons,
  borderless panels, tab bar styling, status bar accent. These serve as
  templates, not requirements.
- A registry so apps can register their own themes and use them by name.

Apps that want no theming at all can skip `apply_theme` and use native styles.
The `DEFAULT_THEME` class attribute on `BaseApplication` controls startup;
 setting
 it to `None` disables qtstrap theming entirely.

### Conventions when a theme IS active

1. Fusion, always, for both standard themes, all platforms. Exotic themes
   may set a different style if it serves the presentation.
2. Theming = `QApplication.setStyle` then `QApplication.setPalette` then
   optionally `QApplication.setStyleSheet`. Nothing else.
3. Never `setPalette` on an individual widget for theming purposes.
4. No per-widget stylesheets in apps. State styling uses dynamic properties
   with rules defined in the theme.
5. Paint code reads `option.palette`/`self.palette()` at paint time, or the
   semantic vocabulary. No hex literals outside theme definitions.
6. Icons are theme-managed (§4.5) — no literal `color=` at `qta.icon` call
   sites.
7. New themes are *registered*, never hardcoded into qtstrap.

### Exotic themes and the application chassis

The [application chassis](plans/application-chassis.md) provides named widget
classes (`ActivityBar`, `Sidebar`, `TabSystem`, `StatusBar`, `Panel`) that
exotic themes can target with QSS selectors. A VSCode-dark theme would style
those classes to reproduce VSCode's visual language:

```css
ActivityBar { background: #333; border: none; }
ActivityBar QToolButton { border: none; padding: 4px; }
StatusBar { background: #007acc; color: white; }
TabSystem::tab-bar { background: #2d2d2d; }
/* etc. */
```

This is why exotic themes depend on the chassis landing first — without
named widget classes, QSS has nothing to target beyond generic `QMainWindow`
and `QWidget`.

---

## 4. The overhaul spec: `extras/style` v2

Implementation order: 4.1 → 4.2 → 4.3 → 4.4 → 4.5 → 4.6. Each step keeps the
existing public API working (`apply_theme(name, app)` remains callable
throughout).

### 4.1 Semantic palette derivation

Replace hand-set palettes with derivation from a small semantic input:

```python
@dataclass
class ThemeColors:
    window: str        # '#353535' — chrome background
    base: str          # '#2a2a2a' — input/view background
    text: str          # '#b4b4b4' — primary text
    accent: str        # '#2a82da' — selections, focus, links
    # optional, derived from the above when omitted:
    disabled_text: str | None = None    # default: text at 55% lightness blend
    tooltip: str | None = None          # default: window
    link: str | None = None             # default: accent


def build_palette(colors: ThemeColors) -> QPalette:
    """Derive a complete QPalette (including the Disabled group and the
    Light/Midlight/Mid/Dark/Shadow bevel roles) from semantic inputs."""
```

Derivation notes for the implementer:

- Bevel roles (`Light`/`Midlight`/`Dark`/`Shadow`) derive by lightening/darkening
  `window` — Fusion uses them for frames and grooves. `QColor.lighter(n)` /
  `.darker(n)` with factors ~150/125/150/300 approximates the stock palettes.
- `Button` = `window`, `ButtonText` = `text`, `AlternateBase` = midpoint of
  `window` and `base`, `HighlightedText` = whichever of black/white contrasts
  with `accent` (compute via lightness, don't hardcode white — the existing
  command-palette bug in one line).
- Disabled group: text roles → `disabled_text`; `Highlight` → desaturated accent.
- Keep the existing `dark()`/`light()` functions as thin wrappers returning
  `build_palette(ThemeColors(...))` with values matching today's palettes as
  closely as possible — this step should be visually near-invisible.

**Edge case:** `QColor` accepts '#rrggbb' strings; validate inputs early and
raise with the offending value — a typo'd hex silently becomes black.

### 4.2 Fixed `apply_theme` + registry

```python
_registry: dict[str, 'Theme'] = {}


@dataclass
class Theme:
    name: str
    palette: Callable[[], QPalette]     # factory, not instance — see edge case
    style: str = 'fusion'
    qss: str = ''                        # optional theme-level stylesheet
    icon_color: str = ''                 # default color for themed icons (§4.5)


def register_theme(theme: Theme) -> None:
    _registry[theme.name] = theme


def available_themes() -> list[str]:
    return list(_registry)


def apply_theme(name: str, app: QApplication) -> None:
    theme = _registry[name]              # KeyError with theme name is fine here
    app.setStyle(theme.style)            # style FIRST (can reset palette)
    app.setPalette(theme.palette())
    if theme.qss:
        app.setStyleSheet(theme.qss)
    else:
        app.setStyleSheet('')            # clear a previous theme's QSS!
    app.style().unpolish(app)
    app.style().polish(app)              # the missing half of the current dance
```

qtstrap registers `dark` and `light` at import; apps register their own before
constructing `BaseApplication`. DeviceManager's bypass becomes:

```python
register_theme(Theme('devicemanager-dark', palette=my_palette_factory))

class Application(BaseApplication):
    DEFAULT_THEME = 'devicemanager-dark'
```

**Edge cases:**
- `palette` is a **factory** because a QPalette constructed before QApplication
  exists can misbehave, and because registration happens at import time.
- Clearing `app.setStyleSheet('')` when the new theme has no QSS is mandatory —
  otherwise switching away from a QSS-bearing theme leaves its rules active.
- `BaseApplication.change_theme` should validate against `available_themes()` and
  fall back to the default with a logged warning — a stale QSettings value from a
  removed theme must not crash startup.
- `ThemeMenu` in `base_window.py` rebuilds from `available_themes()` instead of
  its hardcoded two actions.

### 4.3 Theme-level QSS (sanctioned, discouraged)

The `qss` field exists for the two legitimate cases: dynamic-property state rules
(§1 Layer 3) and the rare palette-inexpressible tweak. Document in its docstring
that every selector added here converts those widgets to QStyleSheetStyle
rendering, and keep qtstrap's built-in themes at `qss=''`.

### 4.4 Theme-aware semantic vocabulary (`colors.py` v2)

`qcolors` becomes a theme-following namespace with the palette-missing semantic
colors, updated by `apply_theme`:

```python
class _SemanticColors:
    success: QColor    # green family, adjusted per theme lightness
    warning: QColor
    error: QColor
    muted: QColor      # de-emphasized text — replaces the qcolors.gray usage
    highlight: QColor  # accent — replaces the command palette's hardcoded cyan

qcolors = _SemanticColors()
```

Each `Theme` carries values for these (with qtstrap defaults derived from the
palette when unspecified). Existing constant-color members (`qcolors.white` etc.)
stay for compatibility but the devtools usages migrate to semantic names — the
scene tree's white-on-light-theme bug (§1 Layer 4) is fixed by switching it to
`palette().text()` / `qcolors.muted`.

**Edge case:** consumers that cached a `QColor` keep the old object — semantic
colors must be *read at use time* like palette colors. Make the attributes
properties resolving against the active theme rather than mutated members, so a
stale read is impossible.

### 4.5 Themed icons

A small helper that makes icons theme-reactive once, for every app:

```python
def themed_icon(name: str, color: str | None = None) -> qta.IconWidgetProxy:
    """qta.icon() that re-resolves on theme change.

    color=None uses the active theme's icon_color. Returns a proxy that
    consumers treat as a QIcon; internally it re-renders when
    App().theme_changed fires.
    """
```

Pragmatic v1 (avoid the proxy complexity): a `ThemedIconMixin` /
`refresh_icons()` protocol — widgets that own icons implement `refresh_icons()`
and register via `App().theme_changed.connect(self.refresh_icons)`; plus
`qta.set_defaults(color=theme.icon_color)` called inside `apply_theme` **before**

**Edge case:** `theme_changed.connect` from widgets needs the connection to die
with the widget — connect with the widget as context/receiver
(`App().theme_changed.connect(self.refresh_icons)` on a method of a QObject does
this automatically; never connect a bare lambda holding `self`).

### 4.6 BaseApplication integration

Ties into [async-guide.md](async-guide.md) §5's declarative-flags design:

- `DEFAULT_THEME: str = 'light'` class attribute (subclass-overridable).
- `change_theme` order: `qta.set_defaults` → `qta.reset_cache()` →
  `apply_theme` → `QSettings().setValue('theme', ...)` → `theme_changed.emit()`.
  (Emit LAST, so consumers re-resolving colors/icons see the new state.)
- Optional `THEME = 'auto'` support: Qt ≥ 6.5 exposes
  `QGuiApplication.styleHints().colorScheme()` and a `colorSchemeChanged` signal —
  map OS dark/light onto registered theme names. Guard by Qt version via
  `qtpy.QT_VERSION`; silently fall back to `DEFAULT_THEME` on older Qt.
- Known limitation to document, not solve: **window title bars.** On Windows the
  title bar follows the OS, not the palette. Qt ≥ 6.5 handles it when the OS is
  in dark mode; forcing dark title bars with a light OS requires platform
  arguments (`-platform windows:darkmode=2`). Out of scope — note it so nobody
  burns a day on it.

---

## 5. Migration checklist

1. Land §4.1 + §4.2 (visually near-invisible; existing apps unaffected).
2. Fix the review's style items against the new system: light-theme Fusion,
   polish call, command palette colors from palette + `qcolors.highlight`
   (bugfix plan P2-14/P2-16), scene tree foregrounds (P2-15 file).
3. Convert DeviceManager: `register_theme` + `DEFAULT_THEME`, delete
   `init_app_style` and `style.py`'s palette (or keep the palette as the
   registered factory). Its `qta.icon(..., color=...)` call sites move to
   `themed_icon`/defaults.
4. Stagehand: no custom palette, so just the icon protocol adoption.
5. Add a smoke test: `apply_theme` each registered theme against a live
   QApplication (offscreen), assert `app.style().objectName() == 'fusion'` and a
   couple of palette roles per theme — this catches the setStyle-resets-palette
   class of regression permanently.
6. Add exotic example themes (vscode-dark, flat-material) once the [application
   chassis](plans/application-chassis.md) lands — they need named widget classes
   to target with QSS. These demonstrate full presentation theming, not just
   palette colors.
7. Delete `extras/style/dark_palette.py` and `extras/style/colors.py` (dead
   code superseded by registry + semantic vocabulary).
