#!/usr/bin/env python
# encoding: utf-8
"""
csvwriter.py

Created by David Peckham on 2009-09-07.
Copyright (c) 2009 David Peckham. All rights reserved.
"""

import sys
import os
import unittest
import csv


class CsvWriter(object):
    
    """Write an inventory of a universe's classes, objects, 
        and conditions to a CSV file

    class, name, id, parent, description, select, where

    """
    
    def __init__(self, universe, csvfile):
        super(CsvWriter, self).__init__()
        self.universe = universe
        self.file = csvfile
        writer = csv.writer(self.file, delimiter=',', quotechar='"', 
            quoting=csv.QUOTE_MINIMAL)
        for c in universe.classes:
            self.write_class(writer, c, '')

    def write_class(self, writer, c, classpath):
        if classpath:
            classpath = classpath + '\\' + c.name
        else:
            classpath = c.name
        writer.writerow((classpath, None, 'class', c.description, None, None))
        for obj in c.objects:
            self.write_object(writer, obj, classpath)
        for condition in c.conditions:
            self.write_condition(writer, condition, classpath)
        for subclass in c.subclasses:
            self.write_class(writer, subclass, classpath)

    def write_object(self, writer, o, classpath):
        writer.writerow((classpath, o.name, 'object', o.description, 
            o.select_sql, o.where_sql))

    def write_condition(self, writer, c, classpath):
        writer.writerow((classpath, c.name, 'condition', c.description, 
            None, c.where_sql))
