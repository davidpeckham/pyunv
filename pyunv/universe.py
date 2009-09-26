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
import collections
from repr import repr


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
        self.contexts = []
        self.parameters = None
        self.table_map = collections.defaultdict(Table.unknown)
        self.object_map = collections.defaultdict(Object.unknown)

    def build_table_map(self):
        """Construct a table map so we can expand where and select clauses"""
        for t in self.tables:
            self.table_map[t.id_] = t

    def build_object_map(self):
        """Construct an object map so we can expand where and select clauses"""
        for c in self.classes:
            self._map_objects(c)
    
    def _map_objects(self, c):
        for o in c.objects:
            self.object_map[o.id_] = o
        for subclass in c.subclasses:
            self._map_objects(subclass)
        

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
    def __init__(self, universe, id_):
        super(Join, self).__init__()
        self.universe = universe
        self.id_ = id_
        self.expression = None
        self.term_count = 0
        self.terms = []
    
    @property
    def statement(self):
        if self.term_count == 2:
            s = self.fullterm(self.terms[0]) + self.expression + self.fullterm(self.terms[1])
        else:
            format = self.expression.replace(chr(1), '%s')
            s = format % tuple([self.fullterm(t) for t in self.terms])
        return s
    
    def fullterm(self, term):
        """return the fully qualified term with table and column names"""
        column_name, table_id = term
        return '%s.%s' % (self.universe.table_map[table_id].name, column_name)


class Context(object):
    
    """docstring for Join"""
    def __init__(self, universe, id_, name, description):
        super(Context, self).__init__()
        self.universe = universe
        self.id_ = id_
        self.name = name
        self.description = description
        self.joins = []

    @property
    def join_list(self):
        return ', '.join([str(join_id) for join_id in self.joins])
        
        
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

    @property
    def fullname(self):
        if self.parent:
            return '%s.%s' % (self.parent.name, self.name)
        else:
            return self.name

    def lookup_table(self, match):
        table_id = int(match.groups()[0])
        return self.universe.table_map[table_id].name
    
    def lookup_object(self, match):
        object_id = int(match.groups()[0])
        return self.universe.object_map[object_id].fullname
    
    def expand_sql(self, sql):
        """Return the SQL with table names instead of table IDs"""
        if sql:
            p = re.compile(r'(?:'+chr(3)+')([0-9]{1,4})')
            expanded_sql = p.sub(self.lookup_table, sql)
            p = re.compile(r'(?:'+chr(2)+')([0-9]{1,4})')
            return p.sub(self.lookup_object, expanded_sql)
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
    
    @classmethod
    def unknown(cls):
        return Object(None, -1, None, "Unknown", "This object has been deleted from the universe")


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

    @property
    def fullname(self):
        if schema:
            return '%s.%s' % (self.schema, self.name)
        else:
            return self.name

    def __str__(self):
        return '%s id=%d, schema=%s name=%s' % (type(self), 
            self.id_, self.schema, self.name) 

    @classmethod
    def unknown(cls):
        return Table(-1, None, "Unknown")
        

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
    def fullname(self):
        if self.parent:
            return '%s.%s' % (self.parent.name, self.name)
        else:
            return self.name

    def __cmp__(self, other):
        return cmp(self.id_, other.id_)
        
    def __str__(self):
        return '%s id=%d, name=%s parent=%d' % (type(self), 
            self.id_, self.name, self.parent) 
        

