`pyunv` is a Python parser for SAP BusinessObjects universe (.unv) files.

Introduction
============

This package reads a SAP BusinessObjects universe (.unv) file
and creates a text manifest that includes universe settings,
classes, objects, conditions, source tables, source columns, and
joins. You can use your favorite diff tool to compare manifests
and track changes between versions of your universes.

Installing
==========

Install PyUnv with easy_install::

    easy_install pyunv

Using
=====

With PyUnv installed, this will create a universe manifest::

    $ python docunv.py tests/universes/universe_xir2.unv
    
or write your own version using pyunv::

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

PyUnv may work with universes created by BusinessObjects XI R3. 
Let me know if you try this.