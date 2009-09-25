from setuptools import setup, find_packages

# python setup.py register sdist upload


SUMMARY = """
PyUnv reads SAP BusinessObjects universe (.unv) files. PyUnv can extract 
universe settings, classes, objects, conditions, and source tables and columns
from the universe file.

PyUnv requires Mako to produce manifests. I include a sample template for a
text manifest. If you come up with your own manifests in RST, HTML, or other,
let me know.
"""

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
    version = '0.2.0',
    
    author='David Peckham',
    author_email = 'dave.peckham@me.com',
    classifiers = filter(None, CLASSIFIERS.split("\n")),
    description = 'Python parser for SAP BusinessObjects universe (*.unv) files',
    download_url = 'http://code.google.com/p/pyunv/downloads/list',
    include_package_data = True,
    install_requires = ['Mako'],
    keywords = ['encoding', 'BusinessObjects', 'SAP', 'universe', 'unv'],
    license = 'LGPL',
    long_description = SUMMARY.strip(),
    #packages = find_packages(exclude=['pyunv.tests']),
    packages = find_packages(),
    platforms = ['Many'],
    provides = ['pyunv'],
    test_suite = 'pyunv.tests',
    url = 'http://code.google.com/p/pyunv/',
    zip_safe = False,
    
    # package_data = {
    #     # If any package contains *.txt or *.rst files, include them:
    #     '': ['*.txt', '*.rst', '*.mako'],
    #     # And include any *.unv files found in the 'tests' package:
    #     'tests': ['*.unv'],
    # },
    
    )
