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
    
    def tearDown(self):
        super(ReaderTests, self).tearDown()
            
    def test_date_from_dateindex1(self):
        date = datetime.date(1976, 7, 4)
        self.assertEqual(Reader.date_from_dateindex(2442964), date)
        
    def test_date_from_dateindex2(self):
        date = datetime.date(1976, 7, 5)
        self.assertEqual(Reader.date_from_dateindex(2442965), date)
        
    def test_date_from_dateindex3(self):
        date = datetime.date(2009, 9, 15)
        self.assertEqual(Reader.date_from_dateindex(2455090), date)
        

class SampleUniverseXIR2(unittest.TestCase):
    
    def setUp(self):
        super(SampleUniverseXIR2, self).setUp()
        self.filename = 'pyunv/tests/universes/universe_xir2.unv'
        self.reader = Reader(open(self.filename, 'rb'))
        self.universe = self.reader.universe
    
    def tearDown(self):
        super(SampleUniverseXIR2, self).tearDown()
        del self.reader

    # tests for universe parameters
    
    def test_universe_name(self):
        self.assertEqual(self.universe.parameters.universe_name, 
            'universe_xir2')
        
    def test_universe_filename(self):
        self.assertEqual(self.universe.parameters.universe_filename, 
            'universe_xir2')
        
    def test_revision(self):
        self.assertEqual(self.universe.parameters.revision, 0)
        
    def test_description(self):
        self.assertEqual(self.universe.parameters.description, 
            'This is the first sample universe for PyUnv tests.'
            ' It uses the pyunv_a database.')
        
    def test_created_by(self):
        self.assertEqual(self.universe.parameters.created_by, 'peckhda')
        
    def test_modified_by(self):
        self.assertEqual(self.universe.parameters.modified_by, 'peckhda')
        
    def test_created_date(self):
        self.assertEqual(self.universe.parameters.created_date, 
            datetime.date(2009, 9, 26))

    def test_modified_date(self):
        self.assertEqual(self.universe.parameters.modified_date, 
            datetime.date(2009, 9, 27))
        
    def test_query_time_limit(self):
        self.assertEqual(self.universe.parameters.query_time_limit, 37)
        
    def test_query_row_limit(self):
        self.assertEqual(self.universe.parameters.query_row_limit, 54321)
        
    def test_cost_estimate_warning_limit(self):
        self.assertEqual(
            self.universe.parameters.cost_estimate_warning_limit, 5)
        
    def test_object_strategy(self):
        self.assertEqual(self.universe.parameters.object_strategy, 
            '(Built-in) Standard Renaming')
        
    def test_long_text_limit(self):
        self.assertEqual(self.universe.parameters.long_text_limit, 1234)
        
    def test_cost_estimate_warning_limit(self):
        self.assertEqual(
            self.universe.parameters.cost_estimate_warning_limit, 5)
        
    def test_comments(self):
        self.assertEqual(self.universe.parameters.comments, 
            'These are comments for the universe_xir2 universe.')
        
    def test_domain(self):
        self.assertEqual(self.universe.parameters.domain, None)

    def test_dbms_engine(self):
        self.assertEqual(self.universe.parameters.dbms_engine, 
            'Generic ODBC3 datasource')

    def test_network_layer(self):
        self.assertEqual(self.universe.parameters.network_layer, 'ODBC')

    # tests for reading universe objects
    
    def test_class_count(self):
        self.assertEqual(self.universe.statistics['classes'], 7)
            
    def test_object_count(self):
        self.assertEqual(self.universe.statistics['objects'], 33)
            
    def test_table_count(self):
        self.assertEqual(self.universe.statistics['tables'], 8)
            
    def test_alias_count(self):
        self.assertEqual(self.universe.statistics['aliases'], 3)
            
    def test_join_count(self):
        self.assertEqual(self.universe.statistics['joins'], 7)
            
    def test_context_count(self):
        self.assertEqual(self.universe.statistics['contexts'], 2)
            
    def test_condition_count(self):
        self.assertEqual(self.universe.statistics['conditions'], 6)

    def test_custom_parameters(self):
        self.assert_(self.universe.custom_parameters['SAMPLE_PARAMETER1'] == '999333')
        self.assert_(self.universe.custom_parameters['OLAP_UNIVERSE'] == 'No')
        self.assert_(self.universe.custom_parameters['ANSI92'] == 'YES')
        self.assert_(self.universe.custom_parameters['SAMPLE_PARAMETER2'] == '999222')
            
    def test_manifest(self):
        Manifest(self.universe).save(open(self.filename+'.txt', 'w'))
        

if __name__ == '__main__':
    unittest.main()
