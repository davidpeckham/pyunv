#!/usr/bin/env python
# encoding: utf-8
"""
test_reader.py

Created by David Peckham on 2009-09-20.
Copyright (c) 2009 David Peckham. All rights reserved.
"""

import datetime
import os
import sys
import unittest

from pyunv.universe import Universe
from pyunv.reader import Reader
from pyunv.manifest import Manifest


class ReaderTests(unittest.TestCase):
    def setUp(self):
        super(ReaderTests, self).setUp()
        self.filename = 'pyunv/tests/test.unv'
        self.reader = Reader(open(self.filename, 'rb'))
    
    def tearDown(self):
        super(ReaderTests, self).tearDown()
        del self.reader
            
    def test_date_from_dateindex1(self):
        date = datetime.date(1976,7,4)
        self.assertEqual(Reader.date_from_dateindex(2442964), date)
        
    def test_date_from_dateindex2(self):
        date = datetime.date(1976,7,5)
        self.assertEqual(Reader.date_from_dateindex(2442965), date)
        
    def test_date_from_dateindex3(self):
        date = datetime.date(2009,9,15)
        self.assertEqual(Reader.date_from_dateindex(2455090), date)
        
    def test_manifest(self):
        universe = self.reader.universe
        f = open(self.filename+'.manifest.txt', 'w')
        manifest = Manifest()
        manifest.save(f, universe)
        f.close()
        

if __name__ == '__main__':
    unittest.main()

