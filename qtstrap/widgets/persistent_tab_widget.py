from qtstrap import *


class PersistentTabWidget(QTabWidget):
    def __init__(self, name, tabs=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        
        self.movable = False
        if 'movable' in kwargs:
            self.movable = kwargs['movable']
            self.tabBar().tabMoved.connect(self.move_tab)

        if tabs:
            if isinstance(tabs, list):
                tab_dict = {}
                for tab in tabs:
                    if hasattr(tab, 'tab_name'):
                        tab_dict[tab.tab_name] = tab
                tabs = tab_dict

            self.restore_state(tabs)

        self.setTabsClosable(True)
        self.tabCloseRequested.connect(self.close_tab)

        self.tabBar().setContextMenuPolicy(Qt.CustomContextMenu)
        self.tabBar().customContextMenuRequested.connect(self.menu)

    def menu(self, pos) -> None:
        menu = QMenu()
        menu.addAction(QAction('Unhide All', self, triggered=self.unhide_all))
        menu.exec_(self.tabBar().mapToGlobal(pos))

    def unhide_all(self):
        for i in range(self.count()):
            self.setTabVisible(i, True)
        QSettings().setValue(self.name + '/visibility', self.visible_tabs())

    def restore_state(self, tabs=None):
        visible_tabs = QSettings().value(self.name + '/visibility', {})

        def add_tab(tab, name):
            self.addTab(tab, name)
            if name in visible_tabs:
                if not visible_tabs[name]:
                    self.setTabVisible(self.count() - 1, False)

        if tabs:
            if self.movable:
                added_tabs = {}
                if prev_tabs := QSettings().value(self.name + '/order', []):
                    for tab in prev_tabs:
                        added_tabs[tab] = tabs[tab]
                        add_tab(tabs[tab], tab)
                    for tab in tabs:
                        if tab not in prev_tabs:
                            add_tab(tabs[tab], tab)
                else:
                    for name, tab in tabs.items():
                        add_tab(tab, name)
            else:
                for name, tab in tabs.items():
                    add_tab(tab, name)

        prev_index = QSettings().value(self.name + '/current', 0)
        if isinstance(prev_index, int):
            self.setCurrentIndex(min(int(prev_index), self.count()))

        self.currentChanged.connect(lambda i: QSettings().setValue(self.name + '/current', i))

    def tab_order(self):
        order = []
        for i in range(self.count()):
            order.append(self.tabText(i))
        return order

    def visible_tabs(self):
        visible = {}
        for i in range(self.count()):
            visible[self.tabText(i)] = self.isTabVisible(i)
        return visible

    def move_tab(self, old, new):
        QSettings().setValue(self.name + '/order', self.tab_order())

    def close_tab(self, index):
        self.setTabVisible(index, False)
        QSettings().setValue(self.name + '/visibility', self.visible_tabs())
