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
from pyunv import __version__


class Universe(object):

    def __init__(self, id_=None, name=None, description=None):
        super(Universe, self).__init__()
        self.pyunv_version = __version__
        self.id_ = id_
        self.name = name
        self.description = description
        self.schema = None
        self.tables = []
        self.virtual_tables = []
        self.columns = []
        self.classes = []
        self.joins = []
        self.contexts = []
        self.parameters = None
        self.custom_parameters = None
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
    
    @property
    def statistics(self):
        
        class Counter(ClassVisitor):
            
            def __init__(self):
                super(Counter, self).__init__()
                self.classes = 0
                self.objects = 0
                self.conditions = 0
            
            def visit_class(self, cls):
                self.classes += 1
            
            def visit_object(self, obj):
                self.objects += 1
            
            def visit_condition(self, cond):
                self.conditions += 1
        
        counter = Counter()
        for c in self.classes:
            c.accept(counter)
        
        stats = dict()
        stats["classes"] = counter.classes
        stats["objects"] = counter.objects
        stats["aliases"] = len([t for t in self.tables if t.is_alias])
        stats["tables"] = len([t for t in self.tables if not t.is_alias])
        stats["joins"] = len(self.joins)
        stats["contexts"] = len(self.contexts)
        # stats["hierarchies"] =
        stats["conditions"] = counter.conditions
        return stats


class Parameters(object):
    
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
        self.query_row_limit = 0
        self.object_strategy = None
        self.cost_estimate_warning_limit = 0
        self.long_text_limit = 0
        self.comments = None
        self.domain = None
        self.dbms_engine = None
        self.network_layer = None


class Class(object):
    
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
    
    def accept(self, visitor):
        visitor.visit_class(self)
        for o in self.objects:
            o.accept(visitor)
        for c in self.conditions:
            c.accept(visitor)
        for s in self.subclasses:
            s.accept(visitor)


class Join(object):
    
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
            s = self.fullterm(self.terms[0]) + self.expression + \
                self.fullterm(self.terms[1])
        else:
            format = self.expression.replace(chr(1), '%s')
            s = format % tuple([self.fullterm(t) for t in self.terms])
        return s
    
    def fullterm(self, term):
        """return the fully qualified term with table and column names"""
        column_name, table_id = term
        return '%s.%s' % (self.universe.table_map[table_id].name, column_name)


class Context(object):
    
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
        self.visible = True
    
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
    
    def __init__(self, universe, id_, parent, name, description):
        super(Object, self).__init__(universe, id_, parent, name, description)
        self.format = None
        self.lov_name = None
    
    @classmethod
    def unknown(cls):
        return Object(None, -1, None, "Unknown", 
            "This object has been deleted from the universe")
    
    def accept(self, visitor):
        visitor.visit_object(self)


class Condition(ObjectBase):
    
    def __init__(self, universe, id_, parent, name, description):
        super(Condition, self).__init__(universe, id_, 
            parent, name, description)
    
    def accept(self, visitor):
        visitor.visit_condition(self)


class Table(object):
    
    def __init__(self, universe, id_, parent_id, name, schema):
        super(Table, self).__init__()
        self.universe = universe
        self.id_ = id_
        self.parent_id = parent_id
        self.name = name
        self.schema = schema
    
    @property
    def fullname(self):
        if self.schema:
            s = '%s.%s' % (self.schema, self.name)
        else:
            s = self.name
        if self.is_alias:
            s += ' (alias for %s)' % self.universe.table_map[
                self.parent_id].fullname
        return s
    
    @property
    def is_alias(self):
        return self.parent_id != 0
    
    def __str__(self):
        return '%s id=%d, schema=%s name=%s' % (type(self),
            self.id_, self.schema, self.name)
    
    @classmethod
    def unknown(cls):
        return Table(None, -1, -1, None, "Unknown")


class VirtualTable(object):
    
    def __init__(self, universe, table_id=None, select=None):
        super(VirtualTable, self).__init__()
        self.universe = universe
        self.table_id = table_id
        self.select = select
    
    def __str__(self):
        return '%s table_id=%d, select=%s' % (type(self),
            self.table_id, self.select)


class Column(object):
    
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


class ClassVisitor(object):
    
    """Visits each node in the class, object, and condition hierarchy"""
    
    def __init__(self):
        super(ClassVisitor, self).__init__()
    
    def visit_class(self, cls):
        """docstring for visit_class"""
        pass
    
    def visit_object(self, obj):
        """docstring for visit_object"""
        pass
    
    def visit_condition(self, condition):
        """docstring for visit_condition"""
        pass
