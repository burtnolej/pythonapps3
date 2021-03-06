
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=20,
          pidlogname=True,proclogname=False)


import unittest
from sqlite3 import IntegrityError as S3IntegrityError, \
     OperationalError as S3OperationalError
import sys

from database_util import Database, tbl_create, tbl_index_count, \
     tbl_index_defn_get, schema_read, schema_get, schema_tbl_get, \
     schema_col_get, schema_tbl_pk_get, schema_print, schema_execute, \
     schema_data_get, tbl_count_get

from database_table_util import tbl_rows_get, tbl_rows_insert, \
     tbl_rows_insert_from_schema, tbl_cols_get, tbl_col_add, \
     dbtblgeneric, tbl_move

sys.path.append("/Users/burtnolej/Development/pythonapps3/utils")
from misc_utils_enum import enum
from os import remove, environ
from time import sleep

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

test_db = enum(name="db_name_test",
               tbl_name="tbl_name_test",
               col_defn=[("col_name1","integer"),
                         ("col_name2","integer"),
                         ("col_name3","integer"),
                         ("col_name4","integer")],
               col_name=["col_name1","col_name2",
                         "col_name3","col_name4",],    
               tbl_pk_defn = ["col_name1","col_name2"],
               tbl_rows=[[1,2,3,4],
                         [5,6,7,8]],
               tbl_rows_1row=[[1,2,3,4]],
               tbl_rows_dupe_key=[[1,2,3,4],
                                 [1,2,7,8]])

test_db_str_1col = enum(name="db_name_test",
                   tbl_name="tbl_name_test",
                   col_defn=[("col_name1","text")],
                   col_name=["col_name1"],
                   tbl_rows=[['\"foobar\"']])

test_db_str = enum(name="db_name_test",
                   tbl_name="tbl_name_test",
                   col_defn=[("col_name1","text"),("col_name2","text")],
                   col_name=["col_name1","col_name2"],
                   tbl_rows=[['\"foobar\"','\"barfoo\"']])

class TestTableRowsGet(unittest.TestCase):
    def setUp(self):
        self.schema_file = environ["PYTHONPATH"] + "/test_misc/test_schema_simple.xml"
    
    def test_tbl_rows_get_spoecific_field(self):

        database = Database(test_db.name)
        
        with database:
            tbl_create(database,test_db.tbl_name,test_db.col_defn)
            tbl_rows_insert(database,test_db.tbl_name,test_db.col_name,
                            test_db.tbl_rows)

        database = Database(test_db.name,True)
        with database:
            col_name,tbl_rows,_ = tbl_rows_get(database,test_db.tbl_name,
                                             ['col_name1','col_name2',
                                              'col_name3','col_name4'])        
            self.assertListEqual(col_name,test_db.col_name)
            self.assertListEqual(tbl_rows,test_db.tbl_rows)
            
    def test_tbl_rows_get_all(self):

        database = Database(test_db.name)
        
        with database:
            tbl_create(database,test_db.tbl_name,test_db.col_defn)
            tbl_rows_insert(database,test_db.tbl_name,test_db.col_name,
                            test_db.tbl_rows)

        database = Database(test_db.name,True)
        with database:
            col_name,tbl_rows,_ = tbl_rows_get(database,test_db.tbl_name)        
            self.assertListEqual(col_name,test_db.col_name)
            self.assertListEqual(tbl_rows,test_db.tbl_rows)
            
class TestTableInsert(unittest.TestCase):
    
    def setUp(self):
        
        self.schema_file = environ["PYTHONPATH"] + "/test_misc/test_schema_simple.xml"
    
    def test_tbl_rows_insert(self):

        database = Database(test_db.name)
        
        with database:
            tbl_create(database,test_db.tbl_name,test_db.col_defn)
            tbl_rows_insert(database,test_db.tbl_name,test_db.col_name,
                            test_db.tbl_rows)

        database = Database(test_db.name,True)
        with database:
            col_name,tbl_rows,_ = tbl_rows_get(database,test_db.tbl_name)        
            self.assertListEqual(col_name,test_db.col_name)
            self.assertListEqual(tbl_rows,test_db.tbl_rows)
            
    def test_tbl_rows_insert_1row(self):

        database = Database(test_db.name)
        
        with database:
            tbl_create(database,test_db.tbl_name,test_db.col_defn)
            tbl_rows_insert(database,test_db.tbl_name,test_db.col_name,
                            test_db.tbl_rows_1row)

        database = Database(test_db.name,True)
        with database:
            col_name,tbl_rows_1row,_ = tbl_rows_get(database,test_db.tbl_name)        
            self.assertListEqual(col_name,test_db.col_name)
            self.assertListEqual(tbl_rows_1row,test_db.tbl_rows_1row)

    def test_tbl_rows_insert_dupe_key(self):

        database = Database(test_db.name, True)

        with database:
            tbl_create(database,test_db.tbl_name,test_db.col_defn, test_db.tbl_pk_defn)

            with self.assertRaises(S3IntegrityError):
                tbl_rows_insert(database,test_db.tbl_name,
                                test_db.col_name,
                                test_db.tbl_rows_dupe_key)
        

class TestTableInsert2(unittest.TestCase):
    
    def setUp(self):
        self.schema_file = environ["PYTHONPATH"] + "/test_misc/test_schema_simple.xml"


    def test_tbl_rows_insert_str_1col(self):

        database = Database(test_db_str_1col.name)
        
        with database:
            tbl_create(database,test_db_str_1col.tbl_name,test_db_str_1col.col_defn)
            tbl_rows_insert(database,test_db_str_1col.tbl_name,test_db_str_1col.col_name,
                            test_db_str_1col.tbl_rows)

        database = Database(test_db_str_1col.name,True)
        with database:
            self.assertEquals('foobar',database.execute("select col_name1 from tbl_name_test",True))


    def test_tbl_rows_insert_str(self):

        database = Database(test_db_str.name)
        
        with database:
            tbl_create(database,test_db_str.tbl_name,test_db_str.col_defn)
            tbl_rows_insert(database,test_db_str.tbl_name,test_db_str.col_name,
                            test_db_str.tbl_rows)

        database = Database(test_db_str.name,True)
        with database:
            self.assertEquals([['foobar','barfoo']],database.execute("select col_name1,col_name2 from tbl_name_test"))

    def test_tbl_rows_insert_from_schema(self):
        
        schema_execute(self.schema_file)
        
        database = Database('fitness')
        
        with database:
            tbl_rows_insert_from_schema(database,self.schema_file,'workout')
            
        database = Database('fitness',True)
            
        with database:
            tbl_col_name, tbl_rows,_ = tbl_rows_get(database,'workout')
            self.assertListEqual(tbl_rows,[[250772, 'cycling'], [260772, 'rowing']])
                
        # this is there to force the delete of the 2nd db created but does
        database = Database('diet',True)
        with database:
            pass
        
class TestTableColumnAdd(unittest.TestCase):
    
    def setUp(self):
        self.schema_file = environ["PYTHONPATH"] +"/test_misc/test_schema_simple.xml"
        
    def test_tbl_cols_get(self):
        
        schema_execute(self.schema_file)
        
        database = Database('fitness', True)
        
        with database:
            self.assertListEqual([('date', 'datetime'), ('type', 'text')],
                                 tbl_cols_get(database,'workout'))
            
        database = Database('diet',True)
        
        with database:
            self.assertListEqual([('name','text'), ('calories','integer')],
                                   tbl_cols_get(database,'food'))
            self.assertListEqual([('type','text'), ('time','datetime')],
                                 tbl_cols_get(database,'meals'))
            
    def test_tbl_col_add(self):
        
        schema_execute(self.schema_file)
        
        database = Database('fitness')
        
        with database:
            tbl_col_add(database,'workout','foobar','text')
        
        database = Database('fitness',True)
            
        with database:
            self.assertListEqual([('date', 'datetime'), ('type', 'text'),('foobar','text')],
                                 tbl_cols_get(database,'workout'))
            
        # this is there to force the delete of the 2nd db created but does
        database = Database('diet',True)
        with database:
            pass
        
class TestDBTblGeneric3_cols_int(unittest.TestCase):

    def setUp(self):
        
        self.database = Database(test_db.name)
        
        class dbtbltest(dbtblgeneric):
            pass

        self.dbg = dbtbltest.datamembers(database=self.database,
                                         dm={'col1':123,'col2':456,'col3':789})
        self.dbg.tbl_name_get()
        self.dbg.tbl_col_defn_get(False)
        self.dbg.tbl_row_value_get(False)
        
    def test_dbobject_get_tblname(self):
        self.assertEquals(self.dbg.tbl_name,'dbtbltest')
        
    def test_dbobject_get_coldefn(self):
        self.assertEquals(self.dbg.tbl_col_defn,[('col1','integer'),('col2','integer'),('col3','integer')])
    
    def test_dbobject_get_colnames(self):
        self.assertEquals(self.dbg.tbl_col_names,['col1','col2','col3'])
    
    def test_dbobject_get_row_value(self):
        self.assertEquals(self.dbg.tbl_row_values,[[123,456,789]])
        
    def test_persist(self):
        with self.database:        
            self.dbg.persist()
        
        self.database = Database(test_db.name,True)
        
        with self.database:
            col_name,tbl_rows,_ = tbl_rows_get(self.database,'dbtbltest',['col1','col2','col3']) 
            self.assertEquals([[123,456,789]],tbl_rows)
               
class TestDBTblGeneric3_cols_str(unittest.TestCase):

    def setUp(self):
        
        self.database = Database(test_db.name)
        
        class dbtbltest(dbtblgeneric):
            pass

        self.dbg = dbtbltest.datamembers(database=self.database,
                                         dm={'col1':"abc",'col2':"def",'col3':"ghi"})
        self.dbg.tbl_name_get()
        self.dbg.tbl_col_defn_get(False)
        self.dbg.tbl_row_value_get(False)
        
    def test_dbobject_get_tblname(self):
        self.assertEquals(self.dbg.tbl_name,'dbtbltest')
        
    def test_dbobject_get_coldefn(self):
        self.assertEquals(self.dbg.tbl_col_defn,[('col1','text'),('col2','text'),('col3','text')])
    
    def test_dbobject_get_colnames(self):
        self.assertEquals(self.dbg.tbl_col_names,['col1','col2','col3'])
    
    def test_dbobject_get_row_value(self):
        self.assertEquals(self.dbg.tbl_row_values,[['"abc"','"def"','"ghi"']])
        
    def test_persist(self):
        with self.database:        
            self.dbg.persist()
        
        self.database = Database(test_db.name,True)

        with self.database:
            col_name,tbl_rows,_ = tbl_rows_get(self.database,'dbtbltest',['col1','col2','col3']) 
            self.assertEquals([['abc','def','ghi']],tbl_rows)

class TestDBTblGeneric1_col_str(unittest.TestCase):

    def setUp(self):
        
        self.database = Database(test_db.name)
        
        class dbtbltest(dbtblgeneric):
            pass

        self.dbg = dbtbltest.datamembers(database=self.database,
                                         dm={'col1':"abc"})
        self.dbg.tbl_name_get()
        self.dbg.tbl_col_defn_get(False)
        self.dbg.tbl_row_value_get(False)
        
    def test_dbobject_get_tblname(self):
        self.assertEquals(self.dbg.tbl_name,'dbtbltest')
        
    def test_dbobject_get_coldefn(self):
        self.assertEquals(self.dbg.tbl_col_defn,[('col1','text')])
    
    def test_dbobject_get_colnames(self):
        self.assertEquals(self.dbg.tbl_col_names,['col1'])
    
    def test_dbobject_get_row_value(self):
        self.assertEquals(self.dbg.tbl_row_values,[['"abc"']])
        
    def test_dbobject_get_dm_values(self):
        # internal dict containing values of data members
        self.assertEquals(self.dbg.dm,{'col1': 'abc'})
        
    def test_persist(self):
        with self.database:        
            self.dbg.persist()
        
        self.database = Database(test_db.name,True)

        with self.database:
            col_name,tbl_rows,_ = tbl_rows_get(self.database,'dbtbltest',['col1']) 
            self.assertEquals([["abc"]],tbl_rows)
            
            
class TestDBTblGeneric_sysinfo(unittest.TestCase):

    def setUp(self):
        
        self.database = Database(test_db.name)
        
        class dbtbltest(dbtblgeneric):
            pass

        self.dbg = dbtbltest.datamembers(database=self.database,
                                         dm={'col1':"abc"})
        self.dbg.tbl_name_get()
        self.dbg.tbl_col_defn_get()
        self.dbg.tbl_row_value_get()
        
        
    def test_dbobject_get_sysinfo_cols(self):
        self.assertEquals(self.dbg.tbl_col_defn,[('col1','text'),
                                                 ('__timestamp','text'),
                                                 ('__id','text')])
        
    def test_dbobject_assert_id(self):
        from datetime import datetime
        with self.database:        
            self.dbg.persist()
        self.database = Database(test_db.name,True)
        with self.database:
            col_name,tbl_rows,_ = tbl_rows_get(self.database,
                                             'dbtbltest',
                                             ['__timestamp','__id']) 
            dt = datetime.strptime(tbl_rows[0][0],"%H:%M:%S")
            
            self.assertAlmostEqual(datetime.now().min,dt.min)
            self.assertAlmostEqual(datetime.now().hour,dt.hour)
            self.assertAlmostEqual(datetime.now().second,dt.second)
                                

class TestDBTblGenericValidateInsertValuesStr(unittest.TestCase):

    def setUp(self):
        
        self.database = Database(test_db.name,True)
        
        class dbtbltest(dbtblgeneric):
            pass

        str = 'foobar'
        self.dbg = dbtbltest.datamembers(database=self.database,
                                         dm={'col1':str})
        self.dbg.tbl_name_get()
        self.dbg.tbl_col_defn_get(False)
        self.dbg.tbl_row_value_get(False)
        
    def test_dbobject_db_str_insert(self):
        # tests that string values are wrapped in quotes
        with self.database:        
            #with self.assertRaises(S3OperationalError):
            self.dbg.persist()
        
class TestDBTblGenericValidateInsertValuesSingleQuotedStr(unittest.TestCase):

    def setUp(self):
        
        self.database = Database(test_db.name)
        
        class dbtbltest(dbtblgeneric):
            pass

        self.dbg = dbtbltest.datamembers(database=self.database,
                                         dm={'col1':'foobar'})
        self.dbg.tbl_name_get()
        self.dbg.tbl_col_defn_get(False)
        self.dbg.tbl_row_value_get(False)
        
    def test_dbobject_db_str_insert(self):
        # tests that string values are wrapped in quotes
        with self.database:        
            #with self.assertRaises(S3OperationalError):
            self.dbg.persist()
                
        self.database = Database(test_db.name,True)

        with self.database:
            col_name,tbl_rows,_ = tbl_rows_get(self.database,'dbtbltest',['col1']) 
            self.assertEquals([['foobar']],tbl_rows)

class TestDBTblGenericValidateInsertValuesDblQuotedStr(unittest.TestCase):

    def setUp(self):
        
        self.database = Database(test_db.name)
        
        class dbtbltest(dbtblgeneric):
            pass

        self.dbg = dbtbltest.datamembers(database=self.database,
                                         dm={'col1':"foobar"})
        self.dbg.tbl_name_get()
        self.dbg.tbl_col_defn_get(False)
        self.dbg.tbl_row_value_get(False)
        
    def test_dbobject_db_str_insert(self):
        # tests that string values are wrapped in quotes
        with self.database:        
            #with self.assertRaises(S3OperationalError):
            self.dbg.persist()
                
        self.database = Database(test_db.name,True)

        with self.database:
            col_name,tbl_rows,_ = tbl_rows_get(self.database,'dbtbltest',['col1']) 
            self.assertEquals([["foobar"]],tbl_rows)

          
class TestDBTblGenericValidateInsertValuesObject(unittest.TestCase):

    def setUp(self):
        
        self.database = Database(test_db.name,True)
        
        class dummy():
            objid='1.1.1'
            
            def __repr__(self):
                return("foobar")
        
        class dbtbltest(dbtblgeneric):
            pass
        
        tmpobj = dummy()

        self.dbg = dbtbltest.datamembers(database=self.database,
                                         dm={'col1':tmpobj})
        self.dbg.tbl_name_get()
        self.dbg.tbl_col_defn_get(False)
        self.dbg.tbl_row_value_get(False)
        
    def test_dbobject_db_obj_insert(self):
        # tests that string values are wrapped in quotes
        with self.database:        
            #with self.assertRaises(Exception):
            self.dbg.persist()

            col_name,tbl_rows,_ = tbl_rows_get(self.database,'dbtbltest',['col1']) 
            self.assertEquals([["1.1.1"]],tbl_rows)
        
class TestDBTblGenericValidateInsertValuesInt(unittest.TestCase):

    def setUp(self):
        
        self.database = Database(test_db.name,True)
        
        class dbtbltest(dbtblgeneric):
            pass
        
        self.dbg = dbtbltest.datamembers(database=self.database,
                                         dm={'col1':123})
        self.dbg.tbl_name_get()
        self.dbg.tbl_col_defn_get(False)
        self.dbg.tbl_row_value_get(False)
        
    def test_dbobject_db_obj_insert(self):
        # tests that string values are wrapped in quotes
        with self.database:        
            #with self.assertRaises(Exception):
            self.dbg.persist()
            
class TestDBTblGenericValidateInsert2RowsSameTable(unittest.TestCase):
    
    # check to see that the table is not created twice
    # will throw up an exception if the test fails
    def setUp(self):
        
        self.database = Database(test_db.name,True)
        
        class dbtbltest(dbtblgeneric):
            pass
        
        self.dbg = dbtbltest.datamembers(database=self.database,
                                         dm={'col1':123})
        self.dbg2 = dbtbltest.datamembers(database=self.database,
                                          dm={'col1':456})
        
    def test_dbobject_no_exception(self):
        with self.database:        
            self.dbg.persist()
            self.dbg2.persist()
            
    def test_dbobject_num_rows(self):
        with self.database:        
            self.dbg.persist()
            self.dbg2.persist()
            
            self.assertEqual(tbl_count_get(self.database,'dbtbltest'),2)
          
class TestDBTblGenericUpdate(unittest.TestCase):
    
    # update a value and store the version in the db
    def setUp(self):
        
        self.database = Database(test_db.name,True)
        
        class dbtbltest(dbtblgeneric):
            pass
        
        self.dbg = dbtbltest.datamembers(database=self.database,
                                         dm={'col1':123})
        
        self.dbg.customtimestamp = "%y%m%d_%H%M%S"
        self.dbg.keepversion = True
        
            
    def test_(self):
        
        expected_results = [[123, u'version'], [678, u'current']]
        
        with self.database:        
            self.dbg.persist()
            origid = self.dbg.id
            
            self.dbg.update('col1',678)
            _,tbl_rows,_ = tbl_rows_get(self.database,'dbtbltest',['col1','__version'])
        
        
        # check the value has been updated
        self.assertEqual(self.dbg.col1,678)
        
        #check the id should have been updated
        newid = self.dbg.id
        self.assertNotEqual(newid,origid) 
        
        # check the db representation
        self.assertListEqual(expected_results,tbl_rows)
        
        # check the internal dict representation
        self.assertEquals(self.dbg.dm,{'col1':678})
        
        
    def test_2updates(self):
        
        expected_results = [[123, u'version'], [678, u'version'], [91011, u'current']]
        
        with self.database:        
            self.dbg.persist()
            origid = self.dbg.id

            self.dbg.update('col1',678)
            self.dbg.update('col1',91011)
            
            _,tbl_rows,_ = tbl_rows_get(self.database,'dbtbltest',['col1','__version'])
        
        
        # check the value has been updated
        self.assertEqual(self.dbg.col1,91011)
        
        #check the id should have been updated
        newid = self.dbg.id
        self.assertNotEqual(newid,origid) 
        
        # check the db representation
        self.assertListEqual(expected_results,tbl_rows)
        
        # check the internal dict representation
        self.assertEquals(self.dbg.dm,{'col1':91011})
        
    def test_str(self):
        
        expected_results = [[123, u'version'], ["def", u'current']]
        
        with self.database:        
            self.dbg.persist()
            origid = self.dbg.id

            self.dbg.update('col1',"\"def\"")
            
            _,tbl_rows,_ = tbl_rows_get(self.database,'dbtbltest',['col1','__version'])
        
        
        # check the value has been updated
        self.assertEqual(self.dbg.col1,"\"def\"")
        
        #check the id should have been updated
        newid = self.dbg.id
        self.assertNotEqual(newid,origid) 
        
        # check the db representation
        self.assertListEqual(expected_results,tbl_rows)
        
    
class TestDBTblGenericUpdateMultiField(unittest.TestCase):
    
    # update a value and store the version in the db
    def setUp(self):
        
        self.database = Database(test_db.name,True)
        
        class dbtbltest(dbtblgeneric):
            pass
        
        self.dbg = dbtbltest.datamembers(database=self.database,
                                         dm={'col1':123,'col2':"abc",'col3':0x434})
        
        self.dbg.customtimestamp = "%y%m%d_%H%M%S"
        self.dbg.keepversion = True
        
            
    def test_(self):
        
        expected_results = [["abc", u'version'], ["foobar", u'current']]
        
        with self.database:        
            self.dbg.persist()
            origid = self.dbg.id
            
            self.dbg.update('col2',"\"foobar\"")
            _,tbl_rows,_ = tbl_rows_get(self.database,'dbtbltest',['col2','__version'])
        
        
        # check the value has been updated
        self.assertEqual(self.dbg.col2,"\"foobar\"")
        
        #check the id should have been updated
        newid = self.dbg.id
        self.assertNotEqual(newid,origid) 
        
        # check the db representation
        self.assertListEqual(expected_results,tbl_rows)
        
        # check the internal dict representation
        self.assertEquals(self.dbg.dm,{'col1':123,'col2':"\"foobar\"",'col3':0x434})
        
class TestDBTblMove(unittest.TestCase):
        
    def setUp(self):
        self.schema_file1 = "/Users/burtnolej/Development/pythonapps/clean/utils/test_misc/test_schema_vsimple.xml"
        schema_execute(self.schema_file1)

        datarows = {'tbl_col_name':[],'tbl_rows':[]}
        
        schema_data_get(self.schema_file1,'workout',datarows)

        self.database1 = Database('fitness')
        
        with self.database1:
            tbl_rows_insert(self.database1,'workout',datarows['tbl_col_name'],datarows['tbl_rows'])
            
        self.schema_file2 = "/Users/burtnolej/Development/pythonapps/clean/utils/test_misc/test_schema_vsimple2.xml"
        schema_execute(self.schema_file2)
        schema_data_get(self.schema_file2,'food',datarows)

        self.database2 = Database('diet')
        
        with self.database2:
            tbl_rows_insert(self.database2,'food',datarows['tbl_col_name'],datarows['tbl_rows'])
            
        
    def test_(self):
        tbl_move(self.database1,self.database2,'workout',True)
        
        expected_results = [[250772, u'cycling'], [260772, u'rowing']]
        
        with self.database2:
            _,rows,_ = tbl_rows_get(self.database2,'workout')        
        
        self.assertListEqual(rows,expected_results)
        
    def tearDown(self):
        
        import os
        try:
            os.remove("fitness.sqlite")
            os.remove("diet.sqlite")
        except:
            pass
        
            
if __name__ == "__main__":

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTableInsert))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTableInsert2))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTableRowsGet))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTableColumnAdd))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBTblGeneric3_cols_int))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBTblGeneric3_cols_str))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBTblGeneric1_col_str))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBTblGeneric_sysinfo))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBTblGenericValidateInsertValuesStr))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBTblGenericValidateInsertValuesObject))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBTblGenericValidateInsertValuesInt))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBTblGenericValidateInsertValuesDblQuotedStr))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBTblGenericValidateInsertValuesSingleQuotedStr))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBTblGenericValidateInsert2RowsSameTable))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBTblMove))

    
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBTblGenericUpdate))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBTblGenericUpdateMultiField))
    
    
    
    unittest.TextTestRunner(verbosity=2).run(suite)
    