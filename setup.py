from distutils.core import setup

# python setup.py register sdist upload

# patch distutils if it can't cope with the "classifiers" or "download_url"
# keywords (prior to python 2.3.0).
from distutils.dist import DistributionMetadata
if not hasattr(DistributionMetadata, 'classifiers'):
    DistributionMetadata.classifiers = None
if not hasattr(DistributionMetadata, 'download_url'):
    DistributionMetadata.download_url = None

readme_text = open("README", "U").read()
    
setup(
    name = 'pyunv',
    version = '0.1.7',
    description = 'Python parser for SAP BusinessObjects universe (*.unv) files',
    long_description = readme_text,
    author='David Peckham',
    author_email = 'dave.peckham@me.com',
    url = 'http://web.me.com/dave.peckham/python/PyUnv.html',
    download_url = 'http://web.me.com/dave.peckham/python/PyUnv_files/',
    license = 'LGPL',
    platforms = ['POSIX', 'Windows'],
    keywords = ['encoding', 'BusinessObjects', 'SAP', 'universe'],
    classifiers = [
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Other Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
    packages = ['pyunv'],
    install_requires = ['Mako'],
    provides = ['pyunv'],
    test_suite = ['pyunv.tests'],
    zip_safe = False,
    )
