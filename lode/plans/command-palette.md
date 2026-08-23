---
type: plan
status: idea
tags: [plan, command-palette, review, paint, multi-stage, frecency]
keywords: [command palette, fuzzy search, paint renderer, multi-stage, frecency, option picker, validation, qsettings]
summary: Thorough review of the command palette — paint renderer issues, multi-stage option chaining, visual feedback for validation, and remaining cleanup.
---

# Plan: Command Palette Review

## Context

The command palette is qtstrap's most complex extras component. It serves as
both a command launcher (VSCode Ctrl+Shift+P) and a generic input surface
(option picker, validated text input, fuzzy search). Recent work added the
option picker mode (`choices` param), frecency sorting with QSettings
persistence, and auto-unregister on command destruction.

This plan covers the remaining issues found during a thorough review.

Related: [application-chassis.md](application-chassis.md) (CommandRegistry as a
chassis component), [bugfix-review-2026-07.md](bugfix-review-2026-07.md) P1-12
(regex crash, fixed), P1-13 (QObject init, fixed), P2-14 (model desync, fixed).

---

## 1. Paint renderer issues

### 1.1 Hardcoded colors

`get_colors()` hardcodes four colors that should come from the palette:

```python
self.selected = QPen(QColor('#FFFFFF'))      # white — invisible on light theme
self.highlight = QPen(QColor('#00d4ff'))     # cyan — hardcoded accent
self.background = QColor('#3d4f5f')          # dark selection bg
self.background = QColor('#b0c4d1')          # light selection bg
```

- `#FFFFFF` selected text is invisible on the light theme's `#b0c4d1` selection
  background.
- `#00d4ff` cyan is hardcoded — should come from the theme's accent/semantic
  color vocabulary (see [../theming-guide.md](../theming-guide.md) §4.4).
- Selection backgrounds should derive from `QPalette.Highlight` with reduced
  saturation, not hardcoded hex values.

**Fix:** read from `QPalette` roles. Use `HighlightedText` for selected, a
semantic accent for highlight matches, and `Highlight` (desaturated) for
selection background. This depends on the theming overhaul's semantic color
vocabulary; in the interim, derive from the palette directly.

### 1.2 `get_colors()` called once, never on theme change

`get_colors()` is called from `reset()`, which is called from `_open()`. If the
theme changes while the palette is open (unlikely but possible), the colors
don't update. The palette should connect to `App().theme_changed` and call
`get_colors()` — but only after the theming overhaul lands.

### 1.3 Text width calculation is implicit

The paint method draws sections left-to-right using `painter.drawText()` return
value (`prev`) to compute the next rect's x position. This works but has no
fallback when the text overflows the item width — long command names with
short prefixes can draw past the right edge, overlapping the shortcut text.

**Fix:** compute total width before drawing; if it exceeds `option.rect.width()`,
either elide or clip. The shortcut text at `Qt.AlignRight` already draws in the
same rect, so collisions are silent — the shortcut overwrites the command text.

### 1.4 `option.rect` mutation

Lines 95-96 mutate `option.rect` in place:
```python
option.rect.setX(option.rect.x() + 5)
option.rect.setWidth(option.rect.width() - 10)
```

`QStyleOptionViewItem` is a shared object — mutating it can affect subsequent
paint calls if the style caches the option. Should copy first:
```python
rect = QRect(option.rect).adjusted(5, 0, -5, 0)
```

### 1.5 Highlight slicing logic is fragile

The section-building logic (lines 115-120) reconstructs the original text by
slicing based on split-part lengths. This works for simple cases but breaks
when the prefix contains characters that `re.split` treats specially even
after escaping — e.g., zero-width matches, or when the prefix appears at
the start/end of the string (empty parts in the split result).

**Fix:** use `str.find()` with accumulated offset instead of `re.split()`.
More robust, no regex needed at all:
```python
def _highlight_sections(self, prefix, value):
    sections = []
    pos = 0
    lower_value = value.lower()
    lower_prefix = prefix.lower()
    while pos < len(value):
        idx = lower_value.find(lower_prefix, pos)
        if idx == -1:
            sections.append(value[pos:])
            break
        if idx > pos:
            sections.append(value[pos:idx])
        sections.append(value[idx:idx + len(prefix)])
        pos = idx + len(prefix)
    return sections
```

---

## 2. Multi-stage option chaining

### Current state

`accept()` calls `self.callback(result)` once and dismisses. There's no way
for the callback to say "show another prompt" without re-invoking the palette
from scratch (which flickers and loses context).

### Desired behavior (VSCode parity)

VSCode chains: "Select a theme" → pick → "Light or Dark?" → pick → done. The
palette stays open, the input clears, the new prompt appears, the user
continues.

### API

```python
# Single-stage (current)
palette.open(cb=my_callback, choices=['a', 'b', 'c'])

# Multi-stage
def step1(result):
    if result == 'theme':
        return {'prompt': 'Light or Dark?', 'choices': ['Light', 'Dark'], 'cb': step2}

def step2(result):
    apply_theme(result)

palette.open(cb=step1, choices=['theme', 'font', 'settings'])
```

The callback returns a dict describing the next prompt. The palette clears the
input, updates the choices/prompt, and stays open. When the callback returns
`None`, the palette dismisses.

### Implementation

In `accept()`, instead of always dismissing:
```python
def accept(self):
    result = ...
    if self.callback:
        next_step = self.callback(result)
        if next_step is not None:
            # Stay open, reconfigure for next step
            self._configure(next_step)
        else:
            self.dismiss()
```

`_configure` re-applies the prompt/choices/validator params without re-opening
the dialog.

---

## 3. Validation visual feedback

### Current state

`validator=` is passed to `QLineEdit.setValidator()`. The QLineEdit shows
native validation feedback (a yellow outline on some platforms), but the
palette doesn't prevent `accept()` on invalid input — pressing Enter returns
the invalid text to the callback.

### Desired behavior

- On invalid input, `accept()` should not call the callback.
- Visual feedback: red border on the QLineEdit when input is invalid.
- Optionally: shake animation on Enter with invalid input (VSCode does this).

### Implementation

```python
def accept(self):
    if self.line.validator():
        if not self.line.hasAcceptableInput():
            # Flash red border, don't accept
            self.line.setStyleSheet('QLineEdit { border: 1px solid red; }')
            call_later(lambda: self.line.setStyleSheet(''), 300)
            return
    # ... proceed with accept
```

---

## 4. Frecency: remaining work

### Current state

`Command` tracks `usage_count` and `last_used`, persists to QSettings.
`CommandModel.sort_commands` sorts matched items by frecency score
(count × recency decay), then alphabetically.

### Remaining

- **Frecency for option picker mode:** plain string choices don't have
  `usage_count`/`last_used`. The `_frecency_score` method handles this via
  `getattr` defaults (returns 0), so strings sort alphabetically. This is
  correct for one-off option pickers, but if the same choices are presented
  repeatedly (e.g. "pick a profile"), persisting selection history would be
  useful. Low priority — defer until a concrete use case appears.

- **QSettings key cleanup:** when a command is unregistered (destroyed),
  its frecency data stays in QSettings forever. Add cleanup in
  `unregister_command`:
  ```python
  QSettings().remove(f'command_palette/{name}')
  ```

- **Recency decay tuning:** current formula is `count / (1 + age_days)`.
  This is a reasonable default. VSCode uses an exponential decay; consider
  `count * exp(-age_days / 7)` for faster forgetting. Defer — the current
  formula works and is simpler to reason about.

---

## 5. Other issues

### 5.1 `completer` param is misleading

`_open()` passes `completer` to `self.line.setCompleter(completer)`, which is
QLineEdit's built-in completion popup. This popup is visually disconnected
from the command palette's own `CommandCompleter` list. The two systems
compete for the same input. Either:
- Remove the `completer` param (the `choices` param covers the same use case
  with the palette's own UI), or
- Document that `completer` is for QLineEdit's native completion only, and
  `choices` is for the palette's fuzzy list.

Recommend removing `completer` — `choices` is strictly better.

### 5.2 `mask` param is niche but useful

`mask=` passes through to `QLineEdit.setInputMask()`. This is the "type an IP
address" use case. It works but should be documented with an example:
```python
palette.open(cb=set_ip, mask='000.000.000.000;_', placeholder='Enter IP address')
```

### 5.3 Singleton + parent=None

`CommandPalette` is `@singleton` — one instance per process. If first
constructed with `parent=None` (global hotkey use case), and later the main
window tries to add it as a child, the parent is already locked. The
`center_on_parent` fix handles the symptom (no crash), but the palette's
lifetime isn't tied to the main window. This is probably fine — the palette
should outlive any single window — but document it.

### 5.4 `WindowDeactivate` dismiss

`eventFilter` dismisses on `WindowDeactivate`. This means clicking outside the
palette closes it — correct for a command palette. But if the palette is
opened from a global hotkey while the app is minimized, `WindowDeactivate`
fires immediately because the app isn't active. Needs testing with the
global hotkey use case.

---

## 6. Implementation order

1. **Fix `option.rect` mutation** (§1.4) — one-line fix, no risk.
2. **Fix highlight slicing** (§1.5) — replace `re.split` with `str.find`.
3. **Remove `completer` param** (§5.1) — superseded by `choices`.
4. **Frecency cleanup on unregister** (§4) — one line in `unregister_command`.
5. **Validation visual feedback** (§3) — red border + reject on invalid.
6. **Multi-stage chaining** (§2) — callback returns next-step dict.
7. **Hardcoded colors** (§1.1-1.2) — wait for theming overhaul, then read
   from palette/semantic vocabulary.
8. **Text overflow** (§1.3) — elide or clip long command names.
9. **Global hotkey testing** (§5.4) — verify `WindowDeactivate` behavior.