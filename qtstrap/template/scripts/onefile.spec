# -*- mode: python ; coding: utf-8 -*-

import sys

sys.path.append('app')

from pathlib import Path
from app_info import AppName, AppIconPath, AppIconName, AppVersion


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
    a.binaries,
    a.zipfiles,
    a.datas,
    name=f'{AppName}_v{AppVersion}',
    icon=Path('..') / AppIconPath / AppIconName,
    debug=False,
    strip=False,
    upx=False,
    runtime_tmpdir=None,
    console=False,
)
