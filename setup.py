#!/usr/bin/python
##
##	   Copyright (c) 2009 David Pekcham
##

"""This package reads a SAP BusinessObjects universe (.unv) file
and creates a text manifest that includes universe settings, 
classes, objects, conditions, source tables, source columns, and 
joins. You can use your favorite diff tool to compare manifests 
and track changes between versions of your universes.
"""

# python setup.py register sdist upload
# python setup.py py2exe

from pyunv import __version__

import sys, os, string
from setuptools import setup, find_packages
from distutils.errors import *

if sys.version_info < (2, 6):
    raise DistutilsError, "This package requires Python 2.6 or later"

if sys.platform[:3] == "win":
    import py2exe

CLASSIFIERS = """
Development Status :: 2 - Pre-Alpha
Environment :: Other Environment
Intended Audience :: Developers
License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)
Natural Language :: English
Operating System :: OS Independent
Programming Language :: Python
Topic :: Software Development :: Libraries :: Python Modules
"""

setup(
    name = 'pyunv',
    version = __version__,
    author = 'David Peckham',
    author_email = 'dave.peckham@me.com',
    classifiers = filter(None, CLASSIFIERS.split("\n")),
    console = ['docunv.py'],
    description = 'Parse SAP BusinessObjects universe (*.unv) files',
    download_url = 'http://code.google.com/p/pyunv/downloads/list',
    include_package_data = True,
    install_requires = ['Mako'],
    keywords = ['BusinessObjects', 'SAP', 'universe', 'unv'],
    license = 'LGPL',
    long_description = __doc__,
    packages = ['pyunv'],
    platforms = ['Many'],
    provides = ['pyunv'],
    test_suite = 'tests',
    url = 'http://code.google.com/p/pyunv/',
    zip_safe = False,
    zipfile = None, # bundle the standard library into the py2exe executable
    )
