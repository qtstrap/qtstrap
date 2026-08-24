from qtpy.QtWidgets import QMenu, QWidget
from qtpy.QtGui import QAction


class CMenu:
    """Context menu builder using a context-manager stack.

    Mirrors qtstrap's context-layout pattern (CVBoxLayout, CHBoxLayout):
    you always call methods on the same object, and ``with`` blocks
    push/pop nested menus via an internal stack.

    ```
    def contextMenuEvent(self, event):
        with CMenu(self, event) as menu:
            menu.add('Reconnect', self._reconnect)
            menu.add('Disconnect', self._disconnect)
            menu.sep()
            with menu.submenu('Advanced'):
                menu.add('Force reconnect', self._force_reconnect)
            action = QAction('Custom', self)
            menu += action
    ```

    The top-level ``with`` block calls ``QMenu.exec(event.globalPos())``
    on exit. Submenu ``with`` blocks add themselves to the parent menu
    and pop the stack on exit.
    """

    def __init__(self, parent=None, event=None):
        self._root_menu = QMenu(parent)
        self._event = event
        self._stack = [self._root_menu]

    def __enter__(self):
        return self

    def __exit__(self, *exc):
        current = self._stack.pop()
        if not self._stack:
            # Root menu exiting — exec if we have an event
            if self._event is not None:
                self._root_menu.exec(self._event.globalPos())
        else:
            # Submenu exiting — add to parent (now at top of stack)
            self._stack[-1].addMenu(current)

    def add(self, text: str, callback=None) -> QAction:
        """Add an action to the current menu level.

        Returns the QAction for further customization (shortcut, checkable, etc.).
        """
        action = self._stack[-1].addAction(text)
        if callback is not None:
            action.triggered.connect(callback)
        return action

    def submenu(self, title: str) -> 'CMenu':
        """Push a submenu onto the stack. Use as a context manager.

        ``with menu.submenu('Advanced'):`` — items added inside the block
        go into the submenu. The submenu is added to the parent on exit.
        """
        sub = QMenu()
        sub.setTitle(title)
        self._stack.append(sub)
        return self

    def sep(self):
        """Add a separator to the current menu level."""
        self._stack[-1].addSeparator()

    def __iadd__(self, action: QAction):
        """Add a pre-built QAction to the current menu level."""
        self._stack[-1].addAction(action)
        return self