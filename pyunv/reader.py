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

sys.path.insert(0, '..')
from pyunv.universe import Universe, Parameters, Class, Join, Object, Condition, Table, VirtualTable, Column

# import pyunv

class Reader(object):
    
    _content_markers = ('Objects;', 'Tables;', 'Columns;', 
        'Virtual Tables;', 'Parameters;', 'Columns Id;', 'Joins;')
    
    def __init__(self, f):
        super(Reader, self).__init__()
        self.file = f
        self.find_content_offsets()
        self.universe = Universe()
        self.universe.parameters = self.read_parameters()
        self.universe.tables = self.read_tables()
        self.universe.table_map = dict()
        for table in self.universe.tables:
            self.universe.table_map[table.id_] = table
        self.universe.virtual_tables = self.read_virtual_tables()
        self.universe.columns = self.read_columns()
        #self.universe.column_attributes = self.read_column_attributes()
        self.universe.joins = self.read_joins()
        self.universe.classes = self.read_classes()
        
    def find_content_offsets(self):
        """find the offsets of the object, table, and column definitions 
        in the BusinessObjects universe file"""
        self.content_offsets = dict()
        contents = self.file.read()
        for marker in Reader._content_markers:
            self.content_offsets[marker] = contents.find(chr(0)+marker) + len(marker) + 1
        del contents
        return
    
    def read_parameters(self):
        """docstring for read_parameters
        
        I unknown (usually 0x22)
        I unknown
        S universe_filename
        S universe_name
        I revision
        H unknown
        S description
        S created_by
        S modified_by
        I created_date
        I modified_date
        I query_time_limit (seconds)
        I row_limit
        S unknown
        S object_strategy
        x unknown
        I cost_estimate_warning_limit (seconds)
        I long_text_limit (characters)
        4x unknown
        S comments
        3I unknown
        S domain
        S dbms_engine
        S network_layer
        
         Other parameter blocks we don't parse yet:
            Parameters_4_1;
            Parameters_5_0;
            Parameters_6_0;
            Parameters_11_5;
        
        """
        self.file.seek(self.content_offsets['Parameters;'])
        
        params = Parameters()
        struct.unpack('<2I', self.file.read(8))
        params.universe_filename = self.read_shortstring()
        params.universe_name = self.read_shortstring()
        params.revision, = struct.unpack('<I', self.file.read(4))
        struct.unpack('<H', self.file.read(2))
        params.description = self.read_shortstring()
        params.created_by = self.read_shortstring()
        params.modified_by = self.read_shortstring()
        created, modified, = struct.unpack('<2I', self.file.read(8))
        params.created_date = Reader.date_from_dateindex(created)
        params.modified_date = Reader.date_from_dateindex(modified)
        seconds, = struct.unpack('<I', self.file.read(4))
        params.query_time_limit = seconds / 60
        params.row_limit, = struct.unpack('<I', self.file.read(4))
        self.read_shortstring()
        params.object_strategy = self.read_shortstring()
        struct.unpack('<x', self.file.read(1))
        seconds, = struct.unpack('<I', self.file.read(4))
        params.cost_estimate_warning_limit = seconds / 60
        params.long_text_limit, = struct.unpack('<I', self.file.read(4))
        struct.unpack('<4x', self.file.read(4))
        params.comments = self.read_shortstring()
        struct.unpack('<3I', self.file.read(12))
        params.domain = self.read_shortstring()
        params.dbms_engine = self.read_shortstring()
        params.network_layer = self.read_shortstring()
        
        return params

    def read_tables(self):
        """read a BusinessObjects schema definition from the universe file

        B unknown (usually 0x1)
        B unknown (usually 0x1 or 0x2)
        S database_username?
        S schema_name
        I max_table_id
        I table_count
        ???B tables

        """
        self.file.seek(self.content_offsets['Tables;'])
        self.file.read(2)
        user_name = self.read_shortstring()
        schema = self.read_shortstring()
        max_table_id, = struct.unpack('<I', self.file.read(4))
        table_count, = struct.unpack('<I', self.file.read(4))
        return [self.read_table(schema) for x in range(table_count)]

    def read_virtual_tables(self):
        """read the virtual table definitions from the universe file

        I virtual_table_count
        ???B virtual_tables

        """
        self.file.seek(self.content_offsets['Virtual Tables;'])
        count, = struct.unpack('<I', self.file.read(4))
        return [self.read_virtualtable() for x in range(count)]

    def read_columns(self):
        """read the list of source database columns from the universe file

        I column_count
        I column_count?
        ???B columns

        """
        self.file.seek(self.content_offsets['Columns Id;'])
        column_count, = struct.unpack('<I', self.file.read(4))
        column_count2, = struct.unpack('<I', self.file.read(4))
        #print('count1 %d  count2 %d' % (column_count, column_count2))
        return [self.read_column() for x in range(column_count2)]
    
    # def read_column_attributes(self):
    #     """read the column attributes (after marker Columns;)"""
    #     pass

    def read_joins(self):
        """docstring for read_joins
        
        2I unknown
        I join_count
        [...joins...]
        I unknown

        """
        self.file.seek(self.content_offsets['Joins;'])
        self.file.read(8)
        join_count, = struct.unpack('<I', self.file.read(4))
        joins = [self.read_join() for x in range(join_count)]
        self.file.read(8)
        return joins

    def read_classes(self):
        """docstring for read_classes"""
        self.file.seek(self.content_offsets['Objects;'])
        class_count, object_count, condition_count, rootclass_count, = \
            struct.unpack('<4I', self.file.read(16))
        return [self.read_class() for x in range(rootclass_count)]
        
    def read_table(self, schema):
        """read a table definition from the universe file

        I table_id
        7x
        3I unknown
        S table_name
        13x
        ? flag
        H count
        xxI unknown (count times)
        
        """
        id_, = struct.unpack('<I', self.file.read(4))
        self.file.read(19)
        name = self.read_shortstring()
        self.file.read(13)
        flag, = struct.unpack('<?', self.file.read(1))
        if flag:
          count, = struct.unpack('<H', self.file.read(2))
          self.file.read(4*count+3)
        else:
          self.file.read(1)
        return Table(id_, name, schema)

    def read_virtualtable(self):
        """read a virtual table definition from the universe file

        I table_id
        S select
        
        """
        table_id, = struct.unpack('<I', self.file.read(4))
        select = self.read_shortstring()
        return VirtualTable(table_id, select)

    def read_column(self):
        """read a column definition from the universe file

        I column_id
        I table_id
        S table_name
        
        """
        id_, = struct.unpack('<I', self.file.read(4))
        parent, = struct.unpack('<I', self.file.read(4))
        name = self.read_shortstring()
        #print(name)
        return Column(id_, name, parent, self.universe)

    def read_class(self):
        """read a BusinessObjects class definition from the universe file

        I subclass_count
        I id
        S name
        I parent
        S description
        7B unknown
        I object_count
        ???B objects
        I condition_count
        ???B conditions
        ???B subclasses

        """
        id_, = struct.unpack('<I', self.file.read(4))
        name = self.read_shortstring()
        parent, = struct.unpack('<I', self.file.read(4))
        description = self.read_shortstring()
        c = Class(self.universe, id_, parent, name, description)
        self.file.seek(7, os.SEEK_CUR)
        object_count, = struct.unpack('<I', self.file.read(4))
        c.objects = [self.read_object() for x in range(object_count)]
        condition_count, = struct.unpack('<I', self.file.read(4))
        c.conditions = [self.read_condition() for x in range(condition_count)]
        subclass_count, = struct.unpack('<I', self.file.read(4))
        c.subclasses = [self.read_class() for x in range(subclass_count)]
        return c

    def read_object(self):
        """read a BusinessObjects object definition from the universe file

        I id
        S name
        I parent
        S description
        H select_table_count
        ?I select_table_ids (repeats select_table_count times)
        H where_table_count
        ?I where_table_ids (repeats where_table_count times)
        S select (starts 03 nn* 2E)
        S where (starts 02 nn* 20)
        S format
        S unknown
        S lov_name
        58B unknown  (LOV settings, hide indicator?)

       """
        id_, = struct.unpack('<I', self.file.read(4))
        name = self.read_shortstring()
        parent, = struct.unpack('<I', self.file.read(4))
        description = self.read_shortstring()
        o = Object(self.universe, id_, parent, name, description)
        select_tablecount, = struct.unpack('<H', self.file.read(2))
        struct.unpack('<%dI' % select_tablecount, self.file.read(4 * select_tablecount))
        where_tablecount, = struct.unpack('<H', self.file.read(2))
        struct.unpack('<%dI' % where_tablecount, self.file.read(4 * where_tablecount))
        o.select = self.read_shortstring()
        o.where = self.read_shortstring()
        o.format = self.read_shortstring()
        unknown2 = self.read_shortstring()
        o.lov_name = self.read_shortstring()
        self.file.seek(58, os.SEEK_CUR)
        return o

    def read_condition(self):
        """read a BusinessObjects condition definition from the universe file

        I id
        S name
        I parent
        S description
        H where_tablecount
        ?I where_table_ids (repeats where_tablecount times)
        H unknown_tablecount
        ?I table_ids (repeats unknown_tablecount times)
        S where

        """
        id_, = struct.unpack('<I', self.file.read(4))
        name = self.read_shortstring()
        parent, = struct.unpack('<I', self.file.read(4))
        description = self.read_shortstring()
        c = Condition(self.universe, id_, parent, name, description)
        where_tablecount, = struct.unpack('<H', self.file.read(2))
        struct.unpack('<%dI' % where_tablecount, self.file.read(4 * where_tablecount))
        unknown_tablecount, = struct.unpack('<H', self.file.read(2))
        struct.unpack('<%dI' % unknown_tablecount, self.file.read(4 * unknown_tablecount))
        c.where = self.read_shortstring()
        return c

    def read_join(self):
        """read a BusinessObjects join definition from the universe file

        6I unknown
        S join_conditions
        2I unknown
        I term_count
        [repeats term_count times]
            S term
            I term_table_id

        """
        self.file.read(24)
        j = Join(self.universe)
        j.expression = self.read_shortstring()
        self.file.read(8)
        j.term_count, = struct.unpack('<I', self.file.read(4))
        j.terms = []
        for i in range(j.term_count):
            term_name = self.read_shortstring()
            term_parent_id, = struct.unpack('<I', self.file.read(4)) 
            j.terms.append((term_name, term_parent_id))
        return j

    def read_shortstring(self):
        """read a short variable-length string from the universe file"""
        length, = struct.unpack('<H', self.file.read(2))
        if length:
            s, = struct.unpack('<%ds' % length, self.file.read(length))
            return unicode(s.translate(None, '\x0d\x0a'), errors='ignore')
        else:
            return None

    @classmethod
    def date_from_dateindex(cls, dateindex):
        """return the date corresponding to the BusinessObjects universe date index"""
        assert dateindex >= 2442964, 'dateindex must be <= 2442964'
        return datetime.date(1976,7,4) + datetime.timedelta(dateindex-2442964)
