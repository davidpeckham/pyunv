#!/usr/bin/env python
# encoding: utf-8
"""
reader.py

Created by David Peckham on 2009-09-07.
Copyright (c) 2009 David Peckham. All rights reserved.
"""

import datetime
import os
import pdb
import repr
import struct
import sys
import unittest

sys.path.insert(0, '..')
from pyunv.universe import Universe, Parameters, Class, Object, Condition, Table, VirtualTable, Column


class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.filename = 'tests/Universe_A8.unv'

    def testDate(self):
        r = Reader(open(self.filename, 'rb'))
        r.date_from_dateindex(2442964)
        datetime.date(1976,7,4)
            
    def testmanifest(self):
        universe = Reader(open(self.filename, 'rb')).universe
        f = open(self.filename+'.manifest.txt', 'w')
        manifest = Manifest()
        manifest.save(f, universe)
        f.close()
        

if __name__ == '__main__':
    unittest.main()

