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
    >>> Manifest().save(open('manifest.txt', 'w'), universe)

This will create a text manifest of the tables, columns, classes, objects, 
and conditions in your universe.

Applications
============

I wrote the earliest versions of PyUnv to extract descriptions for classes, 
objects, and conditions from the universe file. After reverse-engineering more 
of the universe file format, I saw PyUnv as a way to workaround limitations of 
the BusinessObjects development tools. For example, BusinessObjects Designer 
provides no support for change tracking. If you want to know what changed 
between two versions of a universe, you open the first universe in one 
Designer window and the second in another window, and then compare them 
visually. That is impractical for all but the simplest universes.

With PyUnv, you can export all of the universe metadata to a text manifest file 
and use your favorite file comparison tool (diff, p4diff, FileMerge, or even 
Microsoft Word) to highlight the differences. To track changes over time, just 
store the manifest with your universe in a version control system.

Features
========

At this point, PyUnv reads basic universe information and classes, objects, 
conditions, tables, and virtual tables from a universe file. The Python objects 
defined in PyUnv mirror the entities from the universe file, and are arranged in 
memory in a tree structure as you would see them in Designer. For objects and 
conditions, you can get the description, select statement, where statement, 
and more.

I'm testing PyUnv with universes created on BusinessObjects XI R2. I haven't
tested it with earlier or later versions. I am still reverse-engineering other 
metadata in the universe file. If you have questions, or would like to help, 
just drop me a line.

Not Yet Supported
=================

Object protection levels
Object show/hide status
