# -*- mode: python ; coding: utf-8 -*-

import sys

sys.path.append('app')

from pathlib import Path
from app_info import AppName, AppIconPath, AppIconName


app_path = Path('../app')


a = Analysis(
    [app_path / 'main.py'],
    pathex=[app_path],
    binaries=[],
    datas=[
        (app_path / 'resources', 'resources'),
    ],
    hiddenimports=[],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=None,
)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=AppName,
    icon=Path('..') / AppIconPath / AppIconName,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    console=False,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=False,
    upx_exclude=[],
    name=AppName,
)
