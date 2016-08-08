
import unittest
import sys

from database_util import Database, tbl_create, tbl_index_count, \
     tbl_index_defn_get, schema_read, schema_get, schema_tbl_get, \
     schema_col_get, schema_tbl_pk_get, schema_print, schema_execute, \
     schema_data_get

sys.path.append("/home/burtnolej/Development/pythonapps3/clean/utils")
from misc_utils import enum, generic
from os import remove

PY2 = sys.version_info[0] == 2
PY3 = sys.version_info[0] == 3

test_db = enum(name="db_name_test",
               tbl_name="tbl_name_test",
               col_defn=[("col_name1","text"),
                         ("col_name2","integer"),
                         ("col_name3","integer"),
                         ("col_name4","integer")],
               tbl_pk_defn = ["col_name1","col_name2"])
    
class TestDatabase(unittest.TestCase):
    
    def test_db_create(self):

        database = Database(test_db.name)
        
        with database:
            tbl_create(database,test_db.tbl_name,test_db.col_defn)

        database = Database(test_db.name,True)
            
        with database:
            self.assertTrue(database.tbl_exists(test_db.tbl_name))

class TestTable(unittest.TestCase):
    
    def setUp(self):
        self.schema_file = "/home/burtnolej/Development/pythonapps3/clean/utils/test_misc/test_schema_simple.xml"
            
    def test_tbl_create_pk(self):
        
        database = Database(test_db.name)
        
        with database:
            tbl_create(database,test_db.tbl_name,test_db.col_defn,test_db.tbl_pk_defn)
            
        database = Database(test_db.name,True)
            
        with database:
            self.assertEquals(1,tbl_index_count(database, test_db.tbl_name))
            
            self.assertListEqual(test_db.tbl_pk_defn,tbl_index_defn_get(database,test_db.tbl_name))  
        
class TestSchema(unittest.TestCase):
    
    def setUp(self):
        self.schema_file = "/home/burtnolej/Development/pythonapps3/clean/utils/test_misc/test_schema_simple.xml"
        
    def test_schema_read(self):
        
        schema = schema_read(self.schema_file)
        self.assertListEqual(schema_get(schema),['diet','fitness'])
        self.assertListEqual(schema_tbl_get(schema,'fitness'),['workout'])
        self.assertListEqual(schema_col_get(schema,'diet','meals'),
                             [('type','text'),('time','datetime')])
        self.assertListEqual(schema_col_get(schema,'diet','food'),
                             [('name','text'),('calories','integer')])
        self.assertListEqual(schema_tbl_pk_get(schema,'fitness','workout'),
                             ['date'])
        
    def test_db_create_from_schema(self):
        schema_execute(self.schema_file)
        
        database = Database('fitness',True)
        with database:
            self.assertTrue(database.tbl_exists('workout'))

        database = Database('diet')
        with database:
            self.assertTrue(database.tbl_exists('food'))

        database = Database('diet',True)
        with database:
            self.assertTrue(database.tbl_exists('meals'))            

    def test_schema_read_rows(self):
        
        tbl_col_name, tbl_rows = schema_data_get(self.schema_file,'workout')
        
        self.assertListEqual(tbl_col_name,['date', 'type'])
        self.assertListEqual(tbl_rows,[('250772', '"cycling"'), ('260772', '"rowing"')])
    

class TestDBObject(unittest.TestCase):

    '''DBObject is fixtures to allow a generic object to write itself into a sqlite3 db'''

    class dbgeneric(generic):
            
        def db_tbl_name_get(self):
            self.db_tbl_name = self.__class__.__name__
        
        def db_tbl_col_defn_get(self):
            self.blah = 31321
            
            self.db_tbl_col_defn = []
            attr = self.attr_get_keyval(include_callable=False,
                                        include_nondataattr=False)

            for _name,_val in attr:
                _type = "text"
                try:
                    int(_val)
                    _type = "integer"
                except ValueError, TypeError:
                    pass
                self.db_tbl_col_defn.append((_name,_type))

    def setUp(self):
        class dbtest(self.dbgeneric):
            pass

        self.dbg = dbtest.datamembers(datamembers={'col1':123,'col2':456,'col3':789})
        self.dbg.db_tbl_name_get()
        self.dbg.db_tbl_col_defn_get()
        
    def test_dbobject_get_tblname(self):
        self.assertEquals(self.dbg.db_tbl_name,'dbtest')
        
    def test_dbobject_get_coldefn(self):
        self.assertEquals(self.dbg.db_tbl_col_defn,[('col1','integer'),
                                                    ('col2','integer'),
                                                    ('col3','integer')])
        
                
if __name__ == "__main__":

    suite = unittest.TestSuite()
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDatabase))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestTable))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestSchema))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestDBObject))

    unittest.TextTestRunner(verbosity=2).run(suite)
    