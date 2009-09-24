#!/usr/bin/env python
# encoding: utf-8
"""
pyunv.py

Created by David Peckham on 2009-09-01.
Copyright (c) 2009 David Peckham. All rights reserved.
"""

import os
import re
import sys


class Universe(object):
    
    """docstring for Universe"""
    def __init__(self, id_=None, name=None, description=None):
        super(Universe, self).__init__()
        self.id_ = id_
        self.name = name
        self.description = description
        self.schema = None
        self.tables = []
        self.columns = []
        self.classes = []
        self.joins = []
        self.parameters = None


class Parameters(object):
    """docstring for Parameters"""
    def __init__(self):
        super(Parameters, self).__init__()
        self.universe_filename = None
        self.universe_name = None
        self.revision = 0
        self.description = None
        self.created_by = None
        self.modified_by = None
        self.created_date = None
        self.modified_date = None
        self.query_time_limit = 0
        self.row_limit = 0
        self.object_strategy = None
        self.cost_estimate_warning_limit = 0
        self.long_text_limit = 0
        self.comments = None
        self.domain = None
        self.dbms_engine = None
        self.network_layer = None


class Class(object):
    
    """docstring for Class"""
    def __init__(self, universe, id_, parent, name, description):
        super(Class, self).__init__()
        self.universe = universe
        self.id_ = id_
        self.parent = parent
        self.name = name
        self.description = description
        self.objects = []
        self.conditions = []
        self.subclasses = []


class Join(object):
    
    """docstring for Join"""
    def __init__(self, universe):
        super(Join, self).__init__()
        self.universe = universe
        self.expression = None
        self.term_count = 0
        self.terms = []
    
    @property
    def statement(self):
        if self.term_count > 2:
            format = self.expression.replace(chr(1), '%s')
            s = format % (t[0] for t in self.terms)
        else:
            s = self.terms[0][0] + self.expression + self.terms[1][0]
        return s


class ObjectBase(object):
    
    """docstring for ObjectBase"""
    def __init__(self, universe, id_, parent, name, description):
        super(ObjectBase, self).__init__()
        assert(universe)
        self.universe = universe
        self.id_ = id_
        self.parent = parent
        self.name = name
        self.description = description
        self.select_table_refs = []
        self.where_table_refs = []
        self.select = None
        self.where = None

    def lookup_table(self, match):
        index = int(match.groups()[0])
        try:
            table = self.universe.table_map[index]
            return table.name
        except KeyError:
            return 'UNKNOWN (%d)' % index
    
    def expand_sql(self, sql):
        """Return the SQL with table names instead of table IDs"""
        if sql:
            p = re.compile(r'(?:'+chr(3)+')([0-9]{1,4})')
            return p.sub(self.lookup_table, sql)
        else:
            return None
        
    @property
    def select_sql(self):
        return self.expand_sql(self.select)

    @property
    def where_sql(self):
        return self.expand_sql(self.where)

    def __str__(self):
        return '%s id=%d, name=%s, select=%s' % (type(self), 
            self.id_, self.name, self.select) 

       
class Object(ObjectBase):
    
    """docstring for Object"""
    def __init__(self, universe, id_, parent, name, description):
        super(Object, self).__init__(universe, id_, parent, name, description)
        self.format = None
        self.lov_name = None
        

class Condition(ObjectBase):
    
    """docstring for Condition"""
    def __init__(self, universe, id_, parent, name, description):
        super(Condition, self).__init__(universe, id_, parent, name, description)


class Table(object):

    """docstring for Table"""
    def __init__(self, id_, name, schema):
        super(Table, self).__init__()
        self.id_ = id_
        self.name = name
        self.schema = schema

    def __str__(self):
        return '%s id=%d, schema=%s name=%s' % (type(self), 
            self.id_, self.schema, self.name) 
        

class VirtualTable(object):

    """docstring for VirtualTable"""
    def __init__(self, table_id=None, select=None):
        super(VirtualTable, self).__init__()
        self.table_id = table_id
        self.select = select

    def __str__(self):
        return '%s table_id=%d, select=%s' % (type(self), 
            self.table_id, self.select) 


class Column(object):

    """docstring for Column"""
    def __init__(self, id_=None, name=None, parent=None, universe=None):
        super(Column, self).__init__()
        self.id_ = id_
        self.name = name
        self.parent = parent
        self.universe = universe

    @property
    def table_name(self):
        try:
            tablename = self.universe.table_map[self.parent].name
        except KeyError:
            tablename = 'UNKNOWN TABLE (%d)' % self.parent
        return tablename

    def __str__(self):
        return '%s id=%d, name=%s parent=%d' % (type(self), 
            self.id_, self.name, self.parent) 
        

