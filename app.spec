# -*- mode: python ; coding: utf-8 -*-
from PyInstaller.utils.hooks import collect_submodules

hiddenimports = []
hiddenimports += collect_submodules('pillow')
hiddenimports += collect_submodules('textual')
hiddenimports += collect_submodules('textual-fspicker')
hiddenimports += collect_submodules('textual-imageview')


a = Analysis(
    ['C:/Users/sebas/Documents/github/randomapps/racistcounter/code/app.py'],
    pathex=[],
    binaries=[],
    datas=[('C:/Users/sebas/Documents/github/randomapps/racistcounter/code/app.tcss', '.'), ('C:/Users/sebas/Documents/github/randomapps/racistcounter/code/icon.png', '.')],
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
    a.binaries,
    a.datas,
    [],
    name='app',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=['C:\\Users\\sebas\\Documents\\github\\randomapps\\racistcounter\\code\\icon.ico'],
)