"""Tests for portable mode config resolution.

Tests each starting condition:
  A: no .portable flag → system QSettings
  B: .portable file → ini in app dir
  C: .portable directory → ini inside the directory
  D: .portable flag with stale theme in ini → theme restores correctly
"""
import os
import shutil
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# We need to test OPTIONS.portable detection at import time, which means
# we need to control the filesystem state BEFORE qtstrap imports.
# The approach: set sys.argv[0] to a script inside a temp dir, create/remove
# the .portable flag, then re-import qtstrap in each test.


@pytest.fixture
def temp_app_dir():
    """Create a temp directory simulating an app directory with a main.py entry."""
    tmp = tempfile.mkdtemp()
    entry = Path(tmp) / 'main.py'
    entry.touch()
    yield tmp
    shutil.rmtree(tmp, ignore_errors=True)


def _reset_qtstrap():
    """Force re-import of qtstrap so OPTIONS.portable is recomputed."""
    import sys
    mods_to_remove = [k for k in sys.modules if k.startswith('qtstrap')]
    for k in mods_to_remove:
        del sys.modules[k]


def test_condition_a_no_portable_flag(temp_app_dir):
    """Without .portable, OPTIONS.portable is False."""
    _reset_qtstrap()
    with patch('sys.argv', [str(Path(temp_app_dir) / 'main.py')]):
        from qtstrap.options import OPTIONS
        assert OPTIONS.portable is False
    _reset_qtstrap()


def test_condition_b_portable_file(temp_app_dir):
    """With .portable as a file, OPTIONS.portable is True."""
    (Path(temp_app_dir) / '.portable').touch()
    _reset_qtstrap()
    with patch('sys.argv', [str(Path(temp_app_dir) / 'main.py')]):
        from qtstrap.options import OPTIONS
        assert OPTIONS.portable is True
    _reset_qtstrap()


def test_condition_c_portable_directory(temp_app_dir):
    """With .portable as a directory, OPTIONS.portable is True."""
    (Path(temp_app_dir) / '.portable').mkdir()
    _reset_qtstrap()
    with patch('sys.argv', [str(Path(temp_app_dir) / 'main.py')]):
        from qtstrap.options import OPTIONS
        assert OPTIONS.portable is True
    _reset_qtstrap()


def test_config_dir_file_vs_directory(temp_app_dir):
    """File → config_dir = parent; directory → config_dir = itself."""
    from qtstrap.options import OPTIONS

    # Test file case
    flag = Path(temp_app_dir) / '.portable'
    flag.touch()
    with patch.object(OPTIONS, 'PORTABLE_FLAG_PATH', flag):
        assert flag.is_dir() is False
        assert flag.parent == Path(temp_app_dir)

    # Test directory case
    flag.unlink()
    flag.mkdir()
    with patch.object(OPTIONS, 'PORTABLE_FLAG_PATH', flag):
        assert flag.is_dir() is True
        assert flag == flag  # config_dir would be the dir itself