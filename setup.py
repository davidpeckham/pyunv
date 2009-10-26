#!/usr/bin/python

##
#  pyunv - Parse SAP BusinessObjects universe (.unv) files
#
#  To upload to PyPi:
#    python setup.py register sdist upload
#  To build Windows executable:
#    python setup.py py2exe
#
#  Copyright (c) 2009 David Peckham
#

from pyunv import __version__ as pyunv_version

import glob
import os
import string
import sys
from setuptools import setup, find_packages
from distutils.errors import *

if sys.version_info < (2, 6):
    raise DistutilsError, "This package requires Python 2.6 or later"

if sys.platform[:3] == "win":
    import py2exe

CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Other Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
    'Natural Language :: English',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Software Development :: Libraries :: Python Modules',
]

description = open("README.txt", "U").read().strip()
changes = open("CHANGES.txt", "U").read().strip()

LONG_DESCRIPTION = description + '\n\n' + changes

OPTIONS = {
    "py2exe": {
        "compressed": 1,
        "optimize": 2,
        "bundle_files": 1,
        "packages": ["pyunv", "mako.cache"],
        "excludes": ["Tkinter"]
        # "dll_excludes": ["MSVCP90.dll",]
        }
}

setup(
    name = 'pyunv',
    version = pyunv_version,
    author = 'David Peckham',
    author_email = 'dave.peckham@me.com',
    classifiers = CLASSIFIERS,
    data_files = [('', glob.glob('*.mako'))],
    description = 'Parse SAP BusinessObjects universe (*.unv) files',
    download_url = 'http://code.google.com/p/pyunv/downloads/list',
    include_package_data = True,
    install_requires = ['Mako'],
    keywords = ['BusinessObjects', 'SAP', 'universe', 'unv'],
    license = 'LGPL',
    long_description = LONG_DESCRIPTION,
    packages = ['pyunv'],
    platforms = ['Many'],
    provides = ['pyunv'],
    test_suite = 'tests',
    url = 'http://code.google.com/p/pyunv/',
    zip_safe = False,
    options = OPTIONS,
    console = ['docunv.py'],
    zipfile = None,
    )
