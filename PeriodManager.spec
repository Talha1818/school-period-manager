# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = ['whitenoise.middleware', 'whitenoise.runserver_nostatic']
hiddenimports += collect_submodules('django.contrib.admin')
hiddenimports += collect_submodules('django.contrib.auth')
hiddenimports += collect_submodules('django.contrib.sessions')
hiddenimports += collect_submodules('django.contrib.messages')
hiddenimports += collect_submodules('django.contrib.staticfiles')
hiddenimports += collect_submodules('timetable')
hiddenimports += collect_submodules('timetable.migrations')
hiddenimports += collect_submodules('config')


a = Analysis(
    ['run_app.py'],
    pathex=[],
    binaries=[],
    datas=[('D:/TimeTableTeacherAssign/period_manager/period_manager/db.sqlite3', '.'), ('D:/TimeTableTeacherAssign/period_manager/period_manager/templates', 'templates'), ('D:/TimeTableTeacherAssign/period_manager/period_manager/static', 'static')],
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='PeriodManager',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='PeriodManager',
)
