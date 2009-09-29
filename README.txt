`pyunv` is a Python parser for SAP BusinessObjects universe (.unv) files.

Introduction
============

PyUnv reads SAP BusinessObjects universe (.unv) files. In BusinessObjects, a 
universe provides a metadata layer above enterprise databases, expressed in 
language that is easier for business users to understand than the underlying 
data structures. Universes are edited with the BusinessObjects Designer and 
saved to universe files in an undocumented binary format. PyUnv can extract 
most of this metadata from the universe file, enabling you to use it outside 
BusinessObjects, or to create tools to streamline your BusinessObjects 
development process.

PyUnv requires Mako to produce manifests. I include a sample template for a
text manifest. If you come up with your own manifests in RST, HTML, or other,
let me know.

Installing
==========

Install PyUnv with easy_install::

    easy_install pyunv

Using
=====

With PyUnv installed, this should work::

    >>> from pyunv.reader import Reader
    >>> from pyunv.manifest import Manifest
    >>> universe = Reader(open('sample.unv', 'rb')).universe
    >>> Manifest(universe).save(open('manifest.txt', 'w'))

This will create a text manifest of the tables, columns, classes, objects, 
and conditions in your universe.

Use diff, FileMerge, or your favorite file comparison tool to compare
manifests so you can track changes between releases.

Limitations
===========

I've tested this with BusinessObjects XI R2 universes. It parses 
most of the information stored in a universe file, but not all. 
Try it on your universes to see if it extracts what you need.

PyUnv will likely not parse universes created in BusinessObjects 6.5.
If it works for your 6.5 universes, please let me know.