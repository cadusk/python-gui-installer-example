# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller spec file for Weather App
Supports: macOS, Windows, Linux
"""

import sys
from PyInstaller.utils.hooks import collect_data_files

# Determine the platform
IS_MACOS = sys.platform == 'darwin'
IS_WINDOWS = sys.platform.startswith('win')
IS_LINUX = sys.platform.startswith('linux')

# Application metadata
APP_NAME = 'WeatherApp'
BUNDLE_IDENTIFIER = 'com.weatherapp.desktop'

# Collect SSL certificates for requests library
datas = collect_data_files('certifi')

# Hidden imports that PyInstaller might miss
hiddenimports = [
    'PyQt6.QtCore',
    'PyQt6.QtGui',
    'PyQt6.QtWidgets',
    'certifi',
    'requests',
]

block_cipher = None

a = Analysis(
    ['weather_app.py'],
    pathex=[],
    binaries=[],
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'tkinter',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(
    a.pure,
    a.zipped_data,
    cipher=block_cipher
)

# Platform-specific icon paths
if IS_WINDOWS:
    icon_file = 'icons/icon.ico'
elif IS_MACOS:
    icon_file = 'icons/icon.icns'
else:  # Linux
    icon_file = 'icons/icon.png'

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name=APP_NAME,
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # GUI app - no console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=icon_file,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name=APP_NAME,
)

# macOS-specific app bundle
if IS_MACOS:
    app = BUNDLE(
        coll,
        name=f'{APP_NAME}.app',
        icon=icon_file,
        bundle_identifier=BUNDLE_IDENTIFIER,
        version='1.0.0',
        info_plist={
            'CFBundleName': APP_NAME,
            'CFBundleDisplayName': 'Weather App',
            'CFBundleShortVersionString': '1.0.0',
            'CFBundleVersion': '1.0.0',
            'CFBundlePackageType': 'APPL',
            'CFBundleSignature': '????',
            'CFBundleExecutable': APP_NAME,
            'CFBundleIdentifier': BUNDLE_IDENTIFIER,
            'NSHighResolutionCapable': 'True',
            'LSMinimumSystemVersion': '10.13.0',
            'NSPrincipalClass': 'NSApplication',
            'NSRequiresAquaSystemAppearance': 'False',
        },
    )
