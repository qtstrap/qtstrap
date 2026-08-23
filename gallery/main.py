"""qtstrap Gallery — a living example app exercising the full framework.

This app showcases:
  - Application chassis: Panel, Sidebar, ActivityBar, StatusBar, TabPanel, Page
  - Context layouts: CVBoxLayout, CHBoxLayout, CFormLayout, CGridLayout
  - Persistent widgets: PersistentLineEdit, PersistentCheckBox, PersistentComboBox
  - SettingsModel: typed settings with QSettings persistence
  - Command palette: command mode + option picker mode
  - AwaitableDialog: the NiceGUI-style await pattern
  - Code editor (if available)
  - Log monitor (if available)
  - Async support: ASYNC=True with qasync + promisio
"""
from qtstrap import *
from qtstrap.chassis import Panel, Sidebar, ActivityBar, StatusBar, StatusBarItem, Page, TabPanel
from qtstrap.extras.settings_model import SettingsModel
from qtstrap.extras.command_palette import CommandPalette, Command

from pydantic import ConfigDict
import time


class AppInfo(BaseAppInfo):
    NAME = 'qtstrap Gallery'
    VERSION = '0.1.0'
    PUBLISHER = 'qtstrap'
    ICON_PATH = ''


# --- Settings Model ---


class GallerySettings(SettingsModel):
    host: str = 'localhost'
    port: str = '8080'
    auto_connect: bool = False
    theme: str = 'dark'

    model_config = ConfigDict(prefix='gallery/settings', validate_assignment=True)


settings = GallerySettings()


# --- Sidebar Panels ---


class ExplorerPanel(Panel):
    name = 'explorer'
    display_name = 'Explorer'
    icon_name = 'fa5s.folder'

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        tree = QTreeWidget()
        tree.setHeaderHidden(True)
        for section in ['Pages', 'Settings', 'Resources']:
            item = QTreeWidgetItem([section])
            tree.addTopLevelItem(item)

        with CVBoxLayout(self, margins=0) as layout:
            layout.add(tree)


class SearchPanel(Panel):
    name = 'search'
    display_name = 'Search'
    icon_name = 'fa5s.search'

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.input = QLineEdit(placeholderText='Search...')
        self.results = QListWidget()

        self.input.textChanged.connect(self._search)

        with CVBoxLayout(self, margins=0) as layout:
            layout.add(self.input)
            layout.add(self.results)

    def _search(self, text):
        self.results.clear()
        if not text:
            return
        # Search registered pages and commands
        from qtstrap.chassis.tab_panel import Page
        from qtstrap.extras.command_palette import CommandRegistry
        for name in Page._registry:
            if text.lower() in name.lower():
                self.results.addItem(f'Page: {name}')
        for cmd in CommandRegistry().commands if hasattr(CommandRegistry, 'commands') else []:
            if text.lower() in cmd.text().lower():
                self.results.addItem(f'Command: {cmd.text()}')


# --- Tab Pages ---


class WelcomePage(Page):
    page_type = 'welcome'
    page_name = 'Welcome'

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        title = QLabel('qtstrap Gallery')
        title.setStyleSheet('font-size: 24px; font-weight: bold;')

        desc = QLabel(
            'This app demonstrates the qtstrap framework features.\n'
            'Use the activity bar on the left to toggle panels.\n'
            'Use the command palette (Ctrl+Shift+P) to run commands.\n'
            'Add pages from the tab context menu.\n'
            'Toggle the theme from the activity bar settings button.'
        )
        desc.setWordWrap(True)

        with CVBoxLayout(self) as layout:
            with layout.hbox(align='center'):
                layout.add(title)
            layout.add(HLine())
            layout.add(desc)
            layout.addStretch()


class WidgetsPage(Page):
    page_type = 'widgets'
    page_name = 'Widgets'

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        with CVBoxLayout(self) as layout:
            layout.add(QLabel('<b>Persistent Widgets</b>'))

            with CFormLayout(layout.add(QWidget())) as form:
                name = PersistentLineEdit('gallery/name', placeholder='your name')
                role = PersistentComboBox('gallery/role', items=['Operator', 'Engineer', 'Researcher'])
                remember = PersistentCheckBox('gallery/remember')
                remember.setText('remember me')
                form.addRow('Name:', name)
                form.addRow('Role:', role)
                form.addRow('', remember)

            layout.add(HLine())

            layout.add(QLabel('<b>Custom Widgets</b>'))

            with CGridLayout(layout.add(QWidget())) as grid:
                play_btn = StateButton(icons=[qta.icon('fa5s.play'), qta.icon('fa5s.pause')])
                auto_toggle = AnimatedToggle()

                grid.addWidget(QLabel('Playback:'), 0, 0)
                grid.addWidget(play_btn, 0, 1)
                grid.addWidget(QLabel('Auto-run:'), 1, 0)
                grid.addWidget(auto_toggle, 1, 1)

            layout.add(HLine())

            layout.add(QLabel('<b>Model-bound Widgets</b>'))

            with CFormLayout(layout.add(QWidget())) as form:
                host_input = PersistentLineEdit('host', model=settings)
                port_input = PersistentLineEdit('port', model=settings)
                auto_check = PersistentCheckBox('auto_connect', model=settings)
                form.addRow('Host:', host_input)
                form.addRow('Port:', port_input)
                form.addRow('Auto-connect:', auto_check)

            layout.addStretch()


class LayoutsPage(Page):
    page_type = 'layouts'
    page_name = 'Layouts'

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        with CVBoxLayout(self) as layout:
            layout.add(QLabel('<b>Context Layouts</b>'))

            with layout.hbox():
                layout.add(QLabel('HBox:'))
                layout.add(QPushButton('A'))
                layout.add(QPushButton('B'))
                layout.add(QPushButton('C'))

            with layout.vbox():
                layout.add(QLabel('VBox:'))
                layout.add(QPushButton('One'))
                layout.add(QPushButton('Two'))

            layout.add(HLine())

            layout.add(QLabel('<b>Splitter</b>'))
            with layout.split('gallery_splitter_demo') as splitter:
                splitter.add(QLabel('Left panel'))
                splitter.add(QLabel('Right panel'))

            layout.add(HLine())

            layout.add(QLabel('<b>Scroll Area</b>'))
            with layout.scroll('gallery_scroll_demo') as scroll:
                for i in range(20):
                    scroll.add(QLabel(f'Item {i}: This is a scrollable list item.'))

            layout.addStretch()


class AsyncPage(Page):
    page_type = 'async'
    page_name = 'Async Demo'

    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.label = QLabel('Ready')
        self.start_btn = QPushButton('Start async task')
        self.start_btn.clicked.connect(self._start)

        self.dialog_btn = QPushButton('Open awaitable dialog')
        self.dialog_btn.clicked.connect(self._open_dialog)

        with CVBoxLayout(self) as layout:
            with layout.hbox():
                layout.add(self.start_btn)
                layout.add(self.dialog_btn)
            layout.add(self.label)
            layout.addStretch()

    def _start(self):
        self.label.setText('Starting...')
        asyncio.create_task(self._run())

    async def _run(self):
        self.label.setText('Running...')
        await asyncio.sleep(2)
        self.label.setText('Done!')

    def _open_dialog(self):
        asyncio.create_task(self._dialog_flow())

    async def _dialog_flow(self):
        from qtstrap.widgets.awaitable_dialog import AwaitableDialog
        dialog = AwaitableDialog(self)
        dialog.setWindowTitle('Confirm')
        dialog.resize(300, 150)

        from qtstrap import CVBoxLayout, QPushButton, QLabel
        result_label = QLabel('Do you want to proceed?')
        yes_btn = QPushButton('Yes')
        no_btn = QPushButton('No')

        yes_btn.clicked.connect(lambda: dialog.submit(True))
        no_btn.clicked.connect(lambda: dialog.submit(False))

        with CVBoxLayout(dialog) as layout:
            layout.add(result_label)
            with layout.hbox(align='center'):
                layout.add(yes_btn)
                layout.add(no_btn)

        result = await dialog
        self.label.setText(f'Dialog result: {result}')


# --- Status Bar Items ---


class ConnectionStatus(StatusBarItem):
    name = 'connection'

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel('●')
        self.label.setStyleSheet('color: green; font-size: 16px;')

        self.text = QLabel('Connected')

        with CHBoxLayout(self, margins=0) as layout:
            layout.add(self.label)
            layout.add(self.text)


class ClockStatus(StatusBarItem):
    name = 'clock'

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.label = QLabel('--:--:--')

        self.timer = QTimer(self)
        self.timer.timeout.connect(self._tick)
        self.timer.start(1000)
        self._tick()

        with CHBoxLayout(self, margins=0) as layout:
            layout.add(self.label)

    def _tick(self):
        self.label.setText(time.strftime('%H:%M:%S'))


# --- Main Window ---


class GalleryWindow(BaseMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.setWindowTitle('qtstrap Gallery')

        # Chassis components
        self.sidebar = Sidebar(self, side='left')
        self.activity_bar = ActivityBar(self, self.sidebar)
        self.tabs = TabPanel(self)
        self.status_bar = StatusBar(self)

        # Theme actions in settings menu
        self.activity_bar.add_settings_action('Light Theme', lambda: App().change_theme('light'))
        self.activity_bar.add_settings_action('Dark Theme', lambda: App().change_theme('dark'))
        self.activity_bar.settings_menu.addSeparator()
        self.activity_bar.add_settings_action('Quit', self.close, 'Ctrl+Q')

        # Command palette
        self.command_palette = CommandPalette(self)
        self.command_palette.action.setShortcut('Ctrl+Shift+P')

        self.commands = [
            Command('Gallery: Add Welcome Page', triggered=lambda: self.tabs.create_page('welcome')),
            Command('Gallery: Add Widgets Page', triggered=lambda: self.tabs.create_page('widgets')),
            Command('Gallery: Add Layouts Page', triggered=lambda: self.tabs.create_page('layouts')),
            Command('Gallery: Add Async Page', triggered=lambda: self.tabs.create_page('async')),
            Command('Gallery: Toggle Theme', triggered=self._toggle_theme),
        ]

        # Load saved tabs
        self.tabs.load()

        # If no tabs, add a welcome page
        if self.tabs.count() == 0:
            self.tabs.create_page('welcome', 'Welcome')

        # Layout: activity bar | sidebar | tabs
        with PersistentCSplitter('gallery/main_split', self, margins=0) as splitter:
            splitter.add(self.sidebar)
            splitter.add(self.tabs)

        self.setMinimumSize(800, 600)
        self.show()

    def _toggle_theme(self):
        current = OPTIONS.theme
        new_theme = 'dark' if current == 'light' else 'light'
        App().change_theme(new_theme)


# --- Application ---


class GalleryApplication(BaseApplication):
    ASYNC = True


def run():
    app = GalleryApplication(app_info=AppInfo)
    window = GalleryWindow()
    app.run()


if __name__ == '__main__':
    run()