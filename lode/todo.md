---
type: domain
tags: [todo, open-issues]
keywords: [dock_widget, adjust_size, AttributeError, rename, lambda, dockLocationChanged]
summary: Open bug in dock_widget.py where a lambda references the missing self.adjust_size, causing AttributeError on dockLocationChanged.
---

- dock_widget.py:19 lambda references self.adjust_size which no longer exists (AttributeError on dockLocationChanged, seen via LogMonitorDockWidget in Stagehand 2026-07-22) — rename casualty, find the new name or delete the hook
