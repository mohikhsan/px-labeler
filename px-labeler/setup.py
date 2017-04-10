"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup
import macholib_patch

APP = ['main.py']
APP_NAME = "PX-Labeler"
DATA_FILES = []
OPTIONS = {
    'argv_emulation': True,
    'iconfile': 'pxgui/icon.icns',
    'bdist_base': '../build/',
    'dist_dir': '../dist/',
    'plist': {
        'CFBundleName': APP_NAME,
        'CFBundleDisplayName': APP_NAME,
        'CFBundleGetInfoString': "Pixelwise image labeler for creating ground truth labels",
        'CFBundleIdentifier': "com.mohikhsan.osx.pxlabeler",
        'CFBundleVersion': "0.1.0",
        'CFBundleShortVersionString': "0.1.0",
        'NSHumanReadableCopyright': u"Copyright © 2017, Mohammad Ikhsan, All Rights Reserved",
    }
}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
