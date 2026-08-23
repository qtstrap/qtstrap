from qtstrap import *
import json


class Page(QWidget):
    """Base class for tab pages with serialization. Subclassing is registration.

    Subclasses define:
        page_type: unique identifier (required, used for save/load)
        page_name: default name for new pages (optional, defaults to page_type)

    Registration is automatic via __init_subclass__. Optional methods:
        serialize() -> dict: return page state for persistence
        deserialize(data: dict): restore page state from persistence
    """
    _registry: dict[str, type['Page']] = {}

    page_type = ''
    page_name = ''

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not getattr(cls, 'page_type', ''):
            raise TypeError(f'{cls.__name__} must define a page_type')
        if cls.page_type in Page._registry:
            raise TypeError(f'{cls.__name__} duplicates page type {cls.page_type!r}')
        Page._registry[cls.page_type] = cls

    def get_name(self) -> str:
        """Return the display name for this page's tab."""
        return self.page_name or self.page_type

    def serialize(self) -> dict:
        """Return page state for persistence. Override in subclasses."""
        return {}

    def deserialize(self, data: dict):
        """Restore page state from persistence. Override in subclasses."""
        pass


class TabPanel(QTabWidget):
    """Main content area with persistent tabs.

    Reads from Page._registry for creating new pages. Supports drag
    reorder, context menu (add/rename/remove), and save/load to JSON.

    Split panels (VSCode-style drag between splits) are explicitly out
    of scope — see the chassis plan.
    """

    def __init__(self, parent=None, name='tabs'):
        super().__init__(parent=parent)
        self._name = name
        self.pages: list[Page] = []

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

        self.tabBar().setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabBar().customContextMenuRequested.connect(self._context_menu)

        # Drag reorder
        self.setMovable(True)

        self._saving_disabled = False

    def create_page(self, page_type: str = None, page_name: str = None) -> Page:
        """Create a new page of the given type and add it."""
        if page_type not in Page._registry:
            raise ValueError(f'Unknown page type: {page_type!r}')

        cls = Page._registry[page_type]
        page = cls()

        if page_name:
            page.page_name = page_name

        self.add(page)
        return page

    def add(self, page: Page):
        """Add a page to the tab panel."""
        self.pages.append(page)
        idx = self.addTab(page, page.get_name())
        self.setCurrentIndex(idx)

    def close_tab(self, index: int):
        """Remove a tab and its page."""
        page = self.widget(index)
        if hasattr(page, 'page_removed'):
            page.page_removed(page)
        self.pages.remove(page)
        self.removeTab(index)
        page.deleteLater()
        self.save()

    def get_unique_page_name(self) -> str:
        """Generate a unique page name."""
        base = 'Page'
        n = 1
        while f'{base} {n}' in [p.get_name() for p in self.pages]:
            n += 1
        return f'{base} {n}'

    def _context_menu(self, pos):
        menu = QMenu()

        # Add page submenu
        add_menu = menu.addAction('Add Page')
        add_submenu = QMenu()
        for page_type in Page._registry:
            action = add_submenu.addAction(page_type)
            action.triggered.connect(lambda checked, t=page_type: self._add_page(t))
        add_menu.setMenu(add_submenu)

        # Rename / remove if right-clicked on a tab
        index = self.tabBar().tabAt(pos)
        if index >= 0:
            menu.addAction('Rename', lambda: self._rename_page(index))
            menu.addAction('Remove', lambda: self.close_tab(index))

        menu.exec_(self.tabBar().mapToGlobal(pos))

    def _add_page(self, page_type: str):
        name = self.get_unique_page_name()
        self.create_page(page_type, name)
        self.save()

    def _rename_page(self, index: int):
        self.setCurrentIndex(index)
        # Simple rename via input dialog
        from qtpy.QtWidgets import QInputDialog
        current_name = self.tabText(index)
        new_name, ok = QInputDialog.getText(self, 'Rename Page', 'Name:', text=current_name)
        if ok and new_name:
            page = self.widget(index)
            if hasattr(page, 'page_name'):
                page.page_name = new_name
            self.setTabText(index, new_name)
            self.save()

    def save(self):
        """Save tab state to QSettings as JSON."""
        if self._saving_disabled:
            return

        data = {
            'tabs': [
                {
                    'type': getattr(page, 'page_type', ''),
                    'name': page.get_name(),
                    'data': page.serialize() if hasattr(page, 'serialize') else {},
                }
                for page in self.pages
            ]
        }
        QSettings().setValue(f'{self._name}/state', json.dumps(data))

    def load(self):
        """Load tab state from QSettings."""
        self._saving_disabled = True

        raw = QSettings().value(f'{self._name}/state', None)
        if raw:
            try:
                data = json.loads(raw) if isinstance(raw, str) else raw
                for tab in data.get('tabs', []):
                    page_type = tab.get('type', '')
                    if page_type in Page._registry:
                        page = self.create_page(page_type, tab.get('name', ''))
                        if hasattr(page, 'deserialize'):
                            page.deserialize(tab.get('data', {}))
            except (json.JSONDecodeError, TypeError):
                pass  # Corrupt data — start fresh

        self._saving_disabled = False
        call_later(self._enable_saving, 250)

    def _enable_saving(self):
        self._saving_disabled = False

    def fix_tab_names(self):
        for i in range(self.count()):
            page = self.widget(i)
            if hasattr(page, 'get_name'):
                self.setTabText(i, page.get_name())