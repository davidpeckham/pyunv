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


class ReaderUniverseXiR2(unittest.TestCase):
    def setUp(self):
        super(ReaderUniverseXiR2, self).setUp()
        self.filename = 'pyunv/tests/universe_xir2.unv'
        self.reader = Reader(open(self.filename, 'rb'))
    
    def tearDown(self):
        super(ReaderUniverseXiR2, self).tearDown()
        del self.reader
            
    def test_manifest(self):
        universe = self.reader.universe
        f = open(self.filename+'.manifest.txt', 'w')
        Manifest().save(f, universe)
        f.close()
        

if __name__ == '__main__':
    unittest.main()

