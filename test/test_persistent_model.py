"""Tests for the model= kwarg on persistent widgets."""
from qtstrap import *
from pydantic import ConfigDict
from qtstrap.extras.settings_model import SettingsModel
import pytest


class AppSettings(SettingsModel):
    name: str = 'default name'
    notes: str = ''
    enabled: bool = False
    index: int = 0

    model_config = ConfigDict(prefix='test_persistent_model')

@pytest.fixture
def settings():
    return AppSettings()


def test_persistent_line_edit_with_model(qtbot, settings):
    settings.name = 'hello from model'
    widget = PersistentLineEdit('name', model=settings)
    qtbot.addWidget(widget)

    assert widget.text() == 'hello from model'

    widget.setText('changed from widget')
    assert settings.name == 'changed from widget'


def test_persistent_check_box_with_model(qtbot, settings):
    settings.enabled = True
    widget = PersistentCheckBox('enabled', model=settings)
    qtbot.addWidget(widget)

    assert widget.isChecked()

    widget.setChecked(False)
    assert settings.enabled == False


def test_persistent_combo_box_with_model(qtbot, settings):
    settings.index = 0
    widget = PersistentComboBox('index', items=['A', 'B', 'C'], model=settings)
    qtbot.addWidget(widget)

    assert widget.currentIndex() == 0

    widget.setCurrentIndex(2)
    assert settings.index == 2


def test_persistent_line_edit_without_model_still_works(qtbot):
    widget = PersistentLineEdit('test/no_model', default='fallback')
    qtbot.addWidget(widget)
    assert widget.text() == 'fallback'


def test_persistent_text_edit_with_model(qtbot, settings):
    settings.notes = 'some notes'
    widget = PersistentTextEdit('notes', model=settings)
    qtbot.addWidget(widget)

    assert widget.toPlainText() == 'some notes'

    widget.setText('updated notes')
    assert settings.notes == 'updated notes'