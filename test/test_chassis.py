"""Tests for the chassis system — Panel, Sidebar, Page, TabPanel, StatusBar."""
import pytest
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QLabel

from qtstrap import *
from qtstrap.chassis import Panel, Sidebar, ActivityBar, StatusBar, StatusBarItem, Page, TabPanel


# --- Panel tests ---


def test_panel_registration(qtbot):
    class TestPanelA(Panel):
        name = 'test_a'

    assert 'test_a' in Panel._registry
    assert Panel._registry['test_a'] is TestPanelA


def test_panel_duplicate_rejected(qtbot):
    class DupPanel(Panel):
        name = 'test_dup'

    with pytest.raises(TypeError, match='duplicates'):
        class DupPanel2(Panel):
            name = 'test_dup'

    del Panel._registry['test_dup']


def test_panel_missing_name_rejected(qtbot):
    with pytest.raises(TypeError, match='must define a name'):
        class BadPanel(Panel):
            pass


def test_panel_display_name_defaults_to_name(qtbot):
    class NamedPanel(Panel):
        name = 'settings'

    panel = NamedPanel()
    assert panel.display_name_resolved == 'settings'

    class DisplayPanel(Panel):
        name = 'custom'
        display_name = 'Custom Panel'

    panel = DisplayPanel()
    assert panel.display_name_resolved == 'Custom Panel'


# --- Sidebar tests ---


def test_sidebar_instantiates_panels(qtbot):
    class SidePanelA(Panel):
        name = 'side_a'

    sidebar = Sidebar()
    qtbot.addWidget(sidebar)

    assert 'side_a' in sidebar.panels()
    assert not sidebar.isVisible()


def test_sidebar_toggle_panel(qtbot):
    class TogglePanel(Panel):
        name = 'toggle_test'

    sidebar = Sidebar()
    qtbot.addWidget(sidebar)

    # Toggle on
    assert sidebar.toggle_panel('toggle_test') is True
    assert sidebar.isVisible()

    # Toggle off
    assert sidebar.toggle_panel('toggle_test') is False
    assert not sidebar.isVisible()


def test_sidebar_unknown_panel(qtbot):
    sidebar = Sidebar()
    qtbot.addWidget(sidebar)

    assert sidebar.toggle_panel('nonexistent') is False
    assert sidebar.current_panel_name() == ''


# --- Page tests ---


def test_page_registration(qtbot):
    class TestPage(Page):
        page_type = 'test_page'

    assert 'test_page' in Page._registry


def test_page_duplicate_rejected(qtbot):
    class DupPage(Page):
        page_type = 'dup_page'

    with pytest.raises(TypeError, match='duplicates'):
        class DupPage2(Page):
            page_type = 'dup_page'


def test_page_missing_type_rejected(qtbot):
    with pytest.raises(TypeError, match='must define a page_type'):
        class BadPage(Page):
            pass


def test_page_get_name_defaults(qtbot):
    class NamedPage(Page):
        page_type = 'my_type'
        page_name = 'My Page'

    page = NamedPage()
    assert page.get_name() == 'My Page'

    class UnnamedPage(Page):
        page_type = 'other_type'

    page = UnnamedPage()
    assert page.get_name() == 'other_type'


# --- TabPanel tests ---


def test_tab_panel_create_page(qtbot):
    class SimplePage(Page):
        page_type = 'simple_create'
        page_name = 'Simple'

    panel = TabPanel()
    qtbot.addWidget(panel)

    page = panel.create_page('simple_create')
    assert page in panel.pages
    assert panel.count() == 1
    assert panel.tabText(0) == 'Simple'


def test_tab_panel_close_tab(qtbot):
    class ClosePage(Page):
        page_type = 'closeable'

    panel = TabPanel()
    qtbot.addWidget(panel)

    panel.create_page('closeable')
    assert panel.count() == 1

    panel.close_tab(0)
    assert panel.count() == 0
    assert len(panel.pages) == 0


def test_tab_panel_unknown_type(qtbot):
    panel = TabPanel()
    qtbot.addWidget(panel)

    with pytest.raises(ValueError, match='Unknown page type'):
        panel.create_page('nonexistent')


def test_tab_panel_add_custom_widget(qtbot):
    """TabPanel should accept plain QWidgets, not just Page subclasses."""
    panel = TabPanel()
    qtbot.addWidget(panel)

    widget = QLabel('custom')
    panel.addTab(widget, 'Custom')
    assert panel.count() == 1


# --- StatusBar tests ---


def test_status_bar_add_item(qtbot):
    class StatusItem(StatusBarItem):
        name = 'test_status'
        def __init__(self, parent=None):
            super().__init__(parent=parent)
            with CVBoxLayout(self, margins=0) as layout:
                self.label = QLabel('OK')
                layout.add(self.label)

    bar = StatusBar(None)
    qtbot.addWidget(bar)

    # Add a custom item to the right side
    custom = QLabel('custom')
    bar.add_item(custom, side='right')
    # Verify the item was added to the toolbar
    assert custom.parent() is bar

# --- ActivityBar tests ---


def test_activity_bar_populates_from_sidebar(qtbot):
    class ActPanel(Panel):
        name = 'act_test'
        display_name = 'Activity'
        icon_name = 'fa5s.cog'

    sidebar = Sidebar()
    qtbot.addWidget(sidebar)

    bar = ActivityBar(None, sidebar)
    qtbot.addWidget(bar)

    assert 'act_test' in bar._buttons
    btn = bar._buttons['act_test']
    assert btn.toolTip() == 'Activity'


def test_activity_bar_has_settings_button(qtbot):
    class SettingsPanel(Panel):
        name = 'settings_test'

    sidebar = Sidebar()
    qtbot.addWidget(sidebar)

    bar = ActivityBar(None, sidebar)
    qtbot.addWidget(bar)

    assert hasattr(bar, 'settings_btn')
    assert bar.settings_btn.toolTip() == 'Settings'