#!/usr/bin/env python
# encoding: utf-8
"""
manifest.py

Created by David Peckham on 2009-09-09.
Copyright (c) 2009 David Peckham. All rights reserved.
"""

import sys
import os
import unittest

from mako.template import Template


class Manifest:
    
    def __init__(self):
        pass

    def save(self, f, universe):
        """docstring for write_manifest"""
        template = Template(filename='pyunv/templates/manifest.mako', 
            output_encoding='utf-8', encoding_errors='replace')
        f.write(template.render(universe=universe))


class ManifestTests(unittest.TestCase):
    
    def setUp(self):
        pass


if __name__ == '__main__':
    unittest.main()
