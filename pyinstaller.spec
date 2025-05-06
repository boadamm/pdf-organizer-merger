"""
PyInstaller spec file for the PDF Tool application.
"""
import os
import sys
from pathlib import Path

# Define the project root directory
# Using Path.cwd() instead of __file__ which isn't available in PyInstaller context
project_root = os.path.abspath(os.getcwd())

# Add project root to sys.path
sys.path.insert(0, project_root)

# Spec file for PyInstaller
a = Analysis(
    ['src/main.py'],
    pathex=[project_root],
    binaries=[],
    datas=[
        # Include assets folder
        (os.path.join(project_root, 'assets'), 'assets'),
    ],
    hiddenimports=[
        'src.core',
        'src.gui',
    ],
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=None)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='PDF-Organizer-Merger',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    icon=os.path.join(project_root, 'assets', 'icon.ico'),
)

# For macOS
app = BUNDLE(
    exe,
    name='PDF-Organizer-Merger.app',
    icon=os.path.join(project_root, 'assets', 'icon.icns'),
    bundle_identifier=None,
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHumanReadableCopyright': 'Copyright © 2023',
    },
) 