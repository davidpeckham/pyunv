#!/usr/bin/env python
# encoding: utf-8
"""
test_reader_sample.py

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


class ReaderSampleTests(unittest.TestCase):
    def setUp(self):
        super(ReaderSampleTests, self).setUp()
        self.filename = 'pyunv/tests/Sample_A.unv'
        self.reader = Reader(open(self.filename, 'rb'))
    
    def tearDown(self):
        super(ReaderSampleTests, self).tearDown()
        del self.reader
            
    def test_manifest(self):
        universe = self.reader.universe
        f = open(self.filename+'.manifest.txt', 'w')
        Manifest().save(f, universe)
        f.close()
        

if __name__ == '__main__':
    unittest.main()

