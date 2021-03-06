#!/usr/bin/python

from sys import path,exit
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import file2list,write_object_to_disk,read_object_from_disk
from collections import OrderedDict
import re
import uniqueid
from gadfly import gadfly
import os,shutil
from uniqueid import UniqueIDGenerator

class Database(object):
    def __init__(self,reset=True):
        self._uniqueidgen = UniqueIDGenerator() # singleton ??
        self._reset = reset
        self._set_db_name()
        self._db_init()

    def _db_init(self):
        self._db_handle = gadfly()
        self._set_dirs()
        self._startup()
        self._get_cursor()

    def _set_db_name(self):
        self._db_name = str(self.__class__).split(".")[1][:-2]
        self._dir_name = "_" + self._db_name + "_dir"
        
    def _startup(self):
        self._db_handle.startup(self._db_name,self._dir_name)
        
    def _get_cursor(self):
        self._cursor = self._db_handle.cursor()
        
    def _commit(self):
        self._db_handle.commit()

    def _close(self):
        self._db_handle.close()

    def _set_dirs(self):
        if self._reset:
            if os.path.exists(self._dir_name):
                shutil.rmtree(self._dir_name)
            os.makedirs(self._dir_name)

    def pp(self):
        return(self._cursor.pp())
        
    def executepp(self,query):
        self._cursor.execute(query)
        print self.pp()

    def execute(self,query):
        self._cursor.execute(query)

    def _get_id(self):
        return(self._uniqueidgen.next())

    @property
    def cursor(self):
        return(self._cursor)
        
    def __call__(self):
        #return(self._cursor)
        return(self)

    def __del__(self):
        self._uniqueidgen.__del__()
        self._commit()
        self._close()
    
#class DataElement(object)

class DataTableSchema(object):
    def __init__(self,**kwargs):
        for key,value in kwargs.iteritems():
            setattr(self,"_el_" + key,value)

class DataTable(object):
    _records = OrderedDict()
    _attributes = []

    def __init__(self,player_schema,db,records):
        self._db = db
        self._set_table_name()
        self._set_attributes(player_schema)
        self._create_in_db(db.cursor)
        self._add_records_in_db(records,db.cursor)

    def _set_table_name(self):
        self._table_name = str(self.__class__).split(".")[1][:-2]
        
    def _add_table(self):
        self._id = self._db._get_id()
        self.__class__._store.append(self._id)

    def get_filemname(self):
        return(str(self.__class__) + ".dat")
        
    def write_to_disk(self):
        pass

    def _set_attributes(self,recordschema):
        count=0
        for attr in recordschema.__dict__.keys():
            if attr.startswith('_el_'):
                attr_name = attr[4:]
                attr_val = getattr(recordschema,attr)
                self._attributes.append((attr_name,attr_val))
            count+=1
                    
    def read_from_disk(self):
        pass

    def add_record(self,record):
        self._records.__setitem__(self._db._get_id,record)

    def _add_records_in_db(self,records,cursor):
        '''
        build an insert record of the format
        C = 'insert into player (attr1,attr2,..n) values (?, ?, n)'
        D = '[(rec1_val1,rec1_val2,..n),(rec2_val1,rec2_val2,..n),n)]'
        execute(C,D)
        '''
        # build the C string
        attr_string = ",".join(str(attr) for attr,datatype in self._attributes)
        qm_string = ",".join('?' for j in range(0,len(self._attributes)))
        exec_string_1 = "insert into " + self._table_name + "(" + attr_string + ") values (" + qm_string + ")"

        val_list = []
        for r in records:
            new_id = self._db._get_id()
            r.insert(0,new_id)
            val_string = tuple(str(field) for field in r)
            val_list.append(val_string)

        exec_string_2 = val_list
        cursor.execute(exec_string_1,exec_string_2)

    def _create_in_db(self,cursor):
        '''
        build a create table record of the format
        'create table Player(id varchar,last_name varchar)
        '''

        # need to add id to the schema
        self._attributes.insert(0,('id','varchar'))
        
        exec_string = "create table " + self._table_name
        attr_string = ",".join(str(attr) + " " + str(dt) for attr,dt in self._attributes)
        exec_string = exec_string + "(" + attr_string + ")"

        cursor.execute(exec_string)


class Football(Database):
    pass

class PlayerSchema(DataTableSchema):
    pass

class Player(DataTable):
    pass

if __name__ == '__main__':

    football = Football()
    exit()
    player_schema = PlayerSchema(last_name = 'varchar',club = 'varchar')
    player_record = [['lineker','leicester city'],
                     ['rooney','manchester united']]
    player = Player(player_schema,football(),player_record)

    football.executepp("select * from Player")
    

 
