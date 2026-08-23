"""Tests for the command palette — option picker, frecency, command mode."""
import time

import pytest
from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication

from qtstrap.extras.command_palette import Command, CommandRegistry, CommandModel


@pytest.fixture
def model():
    return CommandModel()


def test_command_registry_register_and_unregister(qtbot):
    """Commands should register on creation and unregister on destruction."""
    reg = CommandRegistry()
    cmd = Command('Test Action')
    reg.register_command(cmd)
    assert 'Test Action' in reg.registry
    assert cmd in reg.commands

    reg.unregister_command('Test Action')
    assert 'Test Action' not in reg.registry
    assert cmd not in reg.commands


def test_command_model_set_source_strings(qtbot, model):
    """CommandModel should accept plain strings as source (option picker mode)."""
    model.set_source(['banana', 'apple', 'cherry'])
    assert model.rowCount(None) == 3
    assert model.data(model.index(0, 0, None), Qt.EditRole) in ('banana', 'apple', 'cherry')


def test_command_model_fuzzy_filter(qtbot, model):
    """Prefix filtering should match case-insensitively."""
    model.set_source(['Banana', 'Apple', 'Cherry'])
    model.sort_commands('app')
    assert model.rowCount(None) == 3  # all items remain, matched first
    assert model.data(model.index(0, 0, None), Qt.EditRole) == 'Apple'


def test_command_model_frecency_sort(qtbot, model):
    """Items with higher frecency should sort first when no prefix."""
    from qtstrap.extras.command_palette.command_palette import Command

    cmd_a = Command('Action A')
    cmd_b = Command('Action B')

    # Give B more usage
    cmd_b.usage_count = 5
    cmd_b.last_used = time.time()

    cmd_a.usage_count = 1
    cmd_a.last_used = time.time() - 86400  # 1 day ago

    model.set_source([cmd_a, cmd_b])
    # B has higher frecency (5 uses, recent) so it should be first
    assert model.data(model.index(0, 0, None), Qt.EditRole) == 'Action B'


def test_command_persists_usage_count(qtbot):
    """Command should load and save usage_count to QSettings."""
    from qtstrap import QSettings

    QSettings().setValue('command_palette/Test Persist/count', 3)
    QSettings().setValue('command_palette/Test Persist/last_used', time.time())

    cmd = Command('Test Persist')
    assert cmd.usage_count == 3
    assert cmd.last_used > 0

    # Clean up
    cmd.usage_count = 0
    QSettings().remove('command_palette/Test Persist')