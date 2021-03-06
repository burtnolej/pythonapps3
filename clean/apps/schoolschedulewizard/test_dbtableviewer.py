import sys
import os
from os import path as ospath

from Tkinter import *
from ttk import *

import unittest

from dbtableviewer import DBTableUI
from database_util import Database
from database_table_util import tbl_rows_get, tbl_cols_get
from misc_utils_objectfactory import ObjFactory
from misc_utils_log import Log

from shutil import copyfile
from os import remove, path

class Test_Grid_Behaviour_Focus(unittest.TestCase):
    def setUp(self):
        
        self.ui = DBTableUI()
        
        parent_name = self.ui.entrygrid.widgets[0][0].winfo_parent()
        self.parent_widget = self.ui.entrygrid.widgets[0][0]._nametowidget(parent_name)
        self.parent_widget.update()
    
    def test_rightarrow_moveright(self):
        
        self.ui.entrygrid.widgets[0][0].event_generate("<Right>")
        _,new_x,new_y = str(self.parent_widget.focus_get()).split(",")
               
        self.assertEqual(new_x,'0')
        self.assertEqual(new_y,'1')
        
    def test_rightarrow_moveright1_down1(self):
        
        self.ui.entrygrid.widgets[0][0].event_generate("<Right>")
        self.parent_widget.focus_get().event_generate("<Down>")
        
        _,new_x,new_y = str(self.parent_widget.focus_get()).split(",")
              
        self.assertEqual(new_x,'1')
        self.assertEqual(new_y,'1')
        
    def tearDown(self):
        self.ui.destroy()
        
class Test_Grid_Behaviour_Update_Entry(unittest.TestCase):
    def setUp(self):
        
        self.ui = DBTableUI()
        
        parent_name = self.ui.entrygrid.widgets[0][0].winfo_parent()
        self.parent_widget = self.ui.entrygrid.widgets[0][0]._nametowidget(parent_name)
        self.parent_widget.update()
        
        self.ui.entrygrid.widgets[0][0].event_generate("<Right>")
        self.parent_widget.focus_get().event_generate("<Down>")
        
        self.widget = self.parent_widget.focus_get()
    
    def test_rightarrow_moveright(self):

        # need to input char by char for the complete to fire
        self.widget.insert(0,'n')
        self.widget.insert(1,'a')

        self.assertEqual(self.widget['style'],'InFocus.Changed.TEntry')
        
    def tearDown(self):
        self.ui.destroy()
        
class Test_Load(unittest.TestCase):

    def setUp(self):
        
        self.ui = DBTableUI()
        self.dbfilename = 'test_dbtableviewer'
        self.ui.dbname_entry_sv.set(self.dbfilename)
        
    def test_update_queue(self):
        
        self.ui.load()

        expected_results = [('dow',1),('lessontype',1),('objtype',1),('period',1),('saveversion',1),('schedule',1),('student',1),('subject',1),('teacher',1),('userobjid',1)]      
        
        values,bgcolor = self.ui.updates_get('entrygrid',ignoreaxes=False)

        self.assertEqual(values[0][:-2], expected_results)
        
    def test_last_widget_values(self):
        
        expected_results = [('dow','dow'),('lessontype','lessontype'),  ('objtype','objtype'), ('period','period'), ('saveversion','saveversion'), ('schedule','schedule'), ('student','student'),('subject','subject'), ('teacher','teacher'),('userobjid','userobjid'),('__timestamp','__timestamp'),('__id','__id')]

        self.ui.load()
               
        values = self.ui.widget_current_values_get('entrygrid',0)
        
        self.assertListEqual(values, expected_results)

        
    def tearDown(self):
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")        
        
class Test_Load_Change_Save(unittest.TestCase):

    def setUp(self):
        
        self.ui = DBTableUI()
        self.dbfilename = 'test_dbtableviewer'
        self.ui.dbname_entry_sv.set(self.dbfilename)
        self.database = Database(self.dbfilename)
        
    def test_update_queue(self):
        
        #expected_results = [[''],[('Thursday',0)]]
        
        expected_results =  [('dow',1),('lessontype',1),('objtype',1),('period',1),('saveversion',1),('schedule',1),('student',1),('subject',1),('teacher',1),('userobjid',1)]      
        
        
        self.ui.load()
        
        self.ui.entrygrid.widgets[1][0].sv.set('Thursday')
        
        #self.ui.process_updates(self.database)

        values,bgcolor = self.ui.updates_get('entrygrid',ignoreaxes=False)

        self.assertListEqual(values[0][:-2], expected_results)
        
    def test_last_widget_values(self):
        # checking the .current_value status
        
        expected_results = [('','Tuesday'),('','wp'),('','lesson'),('','8:30-9:10'),('',0),('',1),('','COBY'),('','MATH'),('','Amelia'),('','1,5,4')]
        
        self.ui.load()
        
        self.ui.entrygrid.widgets[1][0].sv.set('Thursday')
        
        values = self.ui.widget_current_values_get('entrygrid',1)
        
        #self.ui.process_updates(self.database)
        
        self.assertListEqual(values[:-2], expected_results)
        
    def test_dbwrite(self):
         
        self.ui.load()
        
        self.ui.entrygrid.widgets[1][0].sv.set('Thursday')
        
        self.ui.process_updates(self.database)
        
        expected_result = [['8:30-9:10','COBY','Amelia','Thursday']]
        
        cols = ['period','student','teacher','dow']
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)
        
        self.assertListEqual(expected_result,rows)
        
    def test_dbwrite_int(self):
        
        self.ui.load()
        
        self.ui.entrygrid.widgets[1][0].sv.set(123)
        
        self.ui.process_updates(self.database)
        
        expected_result = [['8:30-9:10','COBY','Amelia','123']]
        
        cols = ['period','student','teacher','dow']
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)
        
        self.assertListEqual(expected_result,rows)
        
    def tearDown(self):
        self.ui.destroy()
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")        
        
class Test_Load_Clear_Load(unittest.TestCase):

    def setUp(self):
        
        self.ui = DBTableUI()
        self.dbfilename = 'test_dbtableviewer'
        self.ui.dbname_entry_sv.set(self.dbfilename)
        self.database = Database(self.dbfilename)
        
    def test_update_queue(self):
        
        expected_results = [('dow',1),('lessontype',1),('objtype',1),('period',1),('saveversion',1),('schedule',1),('student',1),('subject',1),('teacher',1),('userobjid',1)]      
        
        self.ui.load()
        
        self.ui.load()
        
        values,bgcolor = self.ui.updates_get('entrygrid',ignoreaxes=False)

        self.assertEqual(values[0][:-2], expected_results)
        
    def tearDown(self):
        self.ui.destroy()
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")   
        
class Test_Load_Insert_Save(unittest.TestCase):

    def setUp(self):
        
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'
        self.dbname = 'test_dbtableviewer'
        self.dbfilename = path.join(dbpath,self.dbname)
        self.ui = DBTableUI()        
        self.ui.dbname_entry_sv.set(self.dbname)
        self.ui.load()  
        self.database = Database(self.dbfilename) 
        
        self.ui.load()
    
        self.ui.newrowgrid.widgets[1][0].sv.set('Wednesday')
        self.ui.newrowgrid.widgets[1][1].sv.set('wp')
        self.ui.newrowgrid.widgets[1][2].sv.set('lesson')
        self.ui.newrowgrid.widgets[1][3].sv.set('9:52-10:32')
        self.ui.newrowgrid.widgets[1][4].sv.set('0')
        self.ui.newrowgrid.widgets[1][5].sv.set('1')
        self.ui.newrowgrid.widgets[1][6].sv.set('ORIG')
        self.ui.newrowgrid.widgets[1][7].sv.set('ELA')
        self.ui.newrowgrid.widgets[1][8].sv.set('Galina')
        self.ui.newrowgrid.widgets[1][9].sv.set('9,9,9')
    
        self.ui.insert(self.database)
        
    def test_update_queue(self):
        
        expected_results = [[('dow',1),('lessontype',1),('objtype',1),('period',1),('saveversion',1),('schedule',1),('student',1),('subject',1),('teacher',1),('userobjid',1)],
                            [('Tuesday',1),('wp',1),('lesson',1),('8:30-9:10',1),('0',1),('1',1),('COBY',1),('MATH',1),('Amelia',1),('1,5,4',1)],
                            [('Wednesday',1),('wp',1),('lesson',1),('9:52-10:32',1),('0',1),('1',1),('ORIG',1),('ELA',1),('Galina',1),('9,9,9',1)]]


        values,bgcolor = self.ui.updates_get('entrygrid',ignoreaxes=False)

        # for inserts we cannot know the __timestamp, __id values so ignore last 2 system fields
        # need to go back and do this properyl

        self.assertEqual(values[0][:-2], expected_results[0])
        self.assertEqual(values[1][:-2], expected_results[1])        
        self.assertEqual(values[2][:-2], expected_results[2])
        
        

    '''def test_last_widget_values(self):
        # checking the .current_value status
        
        expected_results = [('','Tuesday'),('','wp'),('','lesson'),('','8:30-9:10'),('',0),('',1),('','COBY'),('','MATH'),('','Amelia'),('','1,5,4')]
                
        values = self.ui.widget_current_values_get('entrygrid',1)
                
        self.assertListEqual(values[:-2], expected_results)
        
        expected_results = [('','Wednesday'),('','wp'),('','lesson'),('','9:52-10:32'),('',0),('',1),('','ORIG'),('','ELA'),('','Galina'),('','9,9,9')]
                        
        values = self.ui.widget_current_values_get('entrygrid',2)
                        
        self.assertListEqual(values[:-2], expected_results)
                
    def test_dbwrite(self):
         
        self.ui.process_updates(self.database)
        
        expected_result = [['8:30-9:10','COBY','Amelia','Tuesday'],
                           ['9:52-10:32','ORIG','Galina','Wednesday']]
        
        cols = ['period','student','teacher','dow']
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)
        
        self.assertListEqual(expected_result,rows)'''
        
    def tearDown(self):
        #os.remove(self.tmpdbname+".sqlite")
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")        
        self.ui.destroy()

class Test_Load_Insert_Change_Save(unittest.TestCase):

    def setUp(self):
        
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'
        self.dbname = 'test_dbtableviewer'
        self.dbfilename = path.join(dbpath,self.dbname)
        self.ui = DBTableUI()        
        self.ui.dbname_entry_sv.set(self.dbname)
        self.ui.load()  
        self.database = Database(self.dbfilename) 
        
        self.ui.load()
    
        self.ui.newrowgrid.widgets[1][0].sv.set('Wednesday')
        self.ui.newrowgrid.widgets[1][1].sv.set('wp')
        self.ui.newrowgrid.widgets[1][2].sv.set('lesson')
        self.ui.newrowgrid.widgets[1][3].sv.set('9:52-10:32')
        self.ui.newrowgrid.widgets[1][4].sv.set('0')
        self.ui.newrowgrid.widgets[1][5].sv.set('1')
        self.ui.newrowgrid.widgets[1][6].sv.set('ORIG')
        self.ui.newrowgrid.widgets[1][7].sv.set('ELA')
        self.ui.newrowgrid.widgets[1][8].sv.set('Galina')
        self.ui.newrowgrid.widgets[1][9].sv.set('9,9,9')
    
        self.ui.insert(self.database)
        
        self.ui.entrygrid.widgets[2][0].sv.set('Thursday')
                        
    def test_update_queue(self):
        
        # version number will be zero as an insert is creating in the db
        # version number only increments as db repr changes
        
        expected_results = [[('dow',1),('lessontype',1),('objtype',1),('period',1),('saveversion',1),('schedule',1),('student',1),('subject',1),('teacher',1),('userobjid',1)],
                            [('Tuesday',1),('wp',1),('lesson',1),('8:30-9:10',1),('0',1),('1',1),('COBY',1),('MATH',1),('Amelia',1),('1,5,4',1)],
                            [('Thursday',2),('wp',1),('lesson',1),('9:52-10:32',1),('0',1),('1',1),('ORIG',1),('ELA',1),('Galina',1),('9,9,9',1)]]

        values,bgcolor = self.ui.updates_get('entrygrid',ignoreaxes=False)

        # for inserts we cannot know the __timestamp, __id values so ignore last 2 system fields
        
        self.assertEqual(values[0][:-2], expected_results[0])
        self.assertEqual(values[1][:-2], expected_results[1])  
        self.assertListEqual(values[2][:-2], expected_results[2]) # no updates for row 2
        
    def test_update_queue_after_process_updates(self):

        # should not change from before updates
        
        self.ui.process_updates(self.database)
        
        expected_results = [[('dow',1),('lessontype',1),('objtype',1),('period',1),('saveversion',1),('schedule',1),('student',1),('subject',1),('teacher',1),('userobjid',1)],
                            [('Tuesday',1),('wp',1),('lesson',1),('8:30-9:10',1),('0',1),('1',1),('COBY',1),('MATH',1),('Amelia',1),('1,5,4',1)],
                            [('Thursday',2),('wp',1),('lesson',1),('9:52-10:32',1),('0',1),('1',1),('ORIG',1),('ELA',1),('Galina',1),('9,9,9',1)]]

        values,bgcolor = self.ui.updates_get('entrygrid',ignoreaxes=False)

        # for inserts we cannot know the __timestamp, __id values so ignore last 2 system fields
        self.assertEqual(values[0][:-2], expected_results[0])
        self.assertEqual(values[1][:-2], expected_results[1])  
        self.assertListEqual(values[2][:-2], expected_results[2]) # no updates for row 2

    def test_last_widget_values(self):
        # checking the .current_value status
        
        expected_results = [('','Tuesday'),('','wp'),('','lesson'),('','8:30-9:10'),('',0),('',1),('','COBY'),('','MATH'),('','Amelia'),('','1,5,4')]
                
        values = self.ui.widget_current_values_get('entrygrid',1)
                
        self.assertListEqual(values[:-2], expected_results)
        
        expected_results = [('','Wednesday'),('','wp'),('','lesson'),('','9:52-10:32'),('',0),('',1),('','ORIG'),('','ELA'),('','Galina'),('','9,9,9')]
                        
        values = self.ui.widget_current_values_get('entrygrid',2)
                        
        self.assertListEqual(values[:-2], expected_results)
                
    def test_dbwrite(self):
         
        self.ui.process_updates(self.database)
        
        expected_result = [['8:30-9:10','COBY','Amelia','Tuesday'],
                           ['9:52-10:32','ORIG','Galina','Thursday']]
        
        cols = ['period','student','teacher','dow']
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)
        
        self.assertListEqual(expected_result,rows)
        
    def tearDown(self):
        #os.remove(self.tmpdbname+".sqlite")
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")        
        self.ui.destroy()
        
class Test_Load_Insert_Change_Save_Insert_Save(unittest.TestCase):

    def setUp(self):
        
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'
        self.dbname = 'test_dbtableviewer'
        self.dbfilename = path.join(dbpath,self.dbname)
        self.ui = DBTableUI()        
        self.ui.dbname_entry_sv.set(self.dbname)
        self.ui.load()  
        self.database = Database(self.dbfilename) 
        
        self.ui.load()
    
        self.ui.newrowgrid.widgets[1][0].sv.set('Wednesday')
        self.ui.newrowgrid.widgets[1][1].sv.set('wp')
        self.ui.newrowgrid.widgets[1][2].sv.set('lesson')
        self.ui.newrowgrid.widgets[1][3].sv.set('9:52-10:32')
        self.ui.newrowgrid.widgets[1][4].sv.set('0')
        self.ui.newrowgrid.widgets[1][5].sv.set('1')
        self.ui.newrowgrid.widgets[1][6].sv.set('ORIG')
        self.ui.newrowgrid.widgets[1][7].sv.set('ELA')
        self.ui.newrowgrid.widgets[1][8].sv.set('Galina')
        self.ui.newrowgrid.widgets[1][9].sv.set('9,9,9')
    
        self.ui.insert(self.database)
        
        self.ui.entrygrid.widgets[2][0].sv.set('Thursday')
        
        self.ui.process_updates(self.database)
        
        self.ui.newrowgrid.widgets[1][0].sv.set('Monday')
        self.ui.newrowgrid.widgets[1][1].sv.set('wp')
        self.ui.newrowgrid.widgets[1][2].sv.set('lesson')
        self.ui.newrowgrid.widgets[1][3].sv.set('9:52-10:32')
        self.ui.newrowgrid.widgets[1][4].sv.set('0')
        self.ui.newrowgrid.widgets[1][5].sv.set('1')
        self.ui.newrowgrid.widgets[1][6].sv.set('JAKE')
        self.ui.newrowgrid.widgets[1][7].sv.set('ELA')
        self.ui.newrowgrid.widgets[1][8].sv.set('Stan')
        self.ui.newrowgrid.widgets[1][9].sv.set('8,8,8')

        self.ui.insert(self.database)
                        
    def test_update_queue(self):
        
        expected_results = [[('dow',1),('lessontype',1),('objtype',1),('period',1),('saveversion',1),('schedule',1),('student',1),('subject',1),('teacher',1),('userobjid',1)],
                            [('Tuesday',1),('wp',1),('lesson',1),('8:30-9:10',1),('0',1),('1',1),('COBY',1),('MATH',1),('Amelia',1),('1,5,4',1)],
                            [('Thursday',1),('wp',1),('lesson',1),('9:52-10:32',1),('0',1),('1',1),('ORIG',1),('ELA',1),('Galina',1),('9,9,9',1)],
                            [('Monday',1),('wp',1),('lesson',1),('9:52-10:32',1),('0',1),('1',1),('JAKE',1),('ELA',1),('Stan',1),('8,8,8',1)]]
        
        values,bgcolor = self.ui.updates_get('entrygrid',ignoreaxes=False)

        # for inserts we cannot know the __timestamp, __id values so ignore last 2 system fields

        self.assertEqual(values[0][:-2], expected_results[0])
        self.assertEqual(values[1][:-2], expected_results[1])        
        self.assertEqual(values[2][:-2], expected_results[2])
        self.assertEqual(values[3][:-2], expected_results[3])
        

    def test_last_widget_values(self):
        # checking the .current_value status
        
        expected_results = [('','Tuesday'),('','wp'),('','lesson'),('','8:30-9:10'),('',0),('',1),('','COBY'),('','MATH'),('','Amelia'),('','1,5,4')]
                
        values = self.ui.widget_current_values_get('entrygrid',1)
                
        self.assertListEqual(values[:-2], expected_results)
        
        expected_results = [('','Thursday'),('','wp'),('','lesson'),('','9:52-10:32'),('',0),('',1),('','ORIG'),('','ELA'),('','Galina'),('','9,9,9')]
                        
        values = self.ui.widget_current_values_get('entrygrid',2)
                        
        self.assertListEqual(values[:-2], expected_results)
        
        expected_results = [('','Monday'),('','wp'),('','lesson'),('','9:52-10:32'),('',0),('',1),('','JAKE'),('','ELA'),('','Stan'),('','8,8,8')]
                
        values = self.ui.widget_current_values_get('entrygrid',3)
                
        self.assertListEqual(values[:-2], expected_results)

                
    def test_dbwrite(self):
         
        self.ui.process_updates(self.database)
        
        expected_result = [['8:30-9:10','COBY','Amelia','Tuesday'],
                           ['9:52-10:32','ORIG','Galina','Thursday'],
                           ['9:52-10:32','JAKE','Stan','Monday']]
        
        cols = ['period','student','teacher','dow']
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)
        
        self.assertListEqual(expected_result,rows)
        
    def tearDown(self):
        #os.remove(self.tmpdbname+".sqlite")
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")        
        self.ui.destroy()


        
class Test_Load_Insert(unittest.TestCase):        
#class Test_InsertRow_onto_Loaded_Rows(unittest.TestCase):
    def setUp(self):
        
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'
        self.dbname = 'test_dbtableviewer'
        self.dbfilename = path.join(dbpath,self.dbname)
        self.ui = DBTableUI()        
        self.ui.dbname_entry_sv.set(self.dbname)
        self.ui.load()
        #self.tmpdbname = path.join(dbpath,'test_tmp')
        #copyfile(dbname+".sqlite",self.tmpdbname+".sqlite")
        #self.database = Database(self.tmpdbname)    
        self.database = Database(self.dbfilename)    
        

    def test_insert_row(self):
        
        self.ui.newrowgrid.widgets[1][0].sv.set('Wednesday')
        self.ui.newrowgrid.widgets[1][1].sv.set('wp')
        self.ui.newrowgrid.widgets[1][2].sv.set('lesson')
        self.ui.newrowgrid.widgets[1][3].sv.set('9:52-10:32')
        self.ui.newrowgrid.widgets[1][4].sv.set('1')
        self.ui.newrowgrid.widgets[1][5].sv.set('1')
        self.ui.newrowgrid.widgets[1][6].sv.set('ORIG')
        self.ui.newrowgrid.widgets[1][7].sv.set('ELA')
        self.ui.newrowgrid.widgets[1][8].sv.set('Galina')
        self.ui.newrowgrid.widgets[1][9].sv.set('9,9,9')
        #self.ui.mainloop()
        
        self.ui.insert(self.database)
        
        print self.ui.updates
        expected_result = [['8:30-9:10','COBY','Amelia','Tuesday'],
                           ['9:52-10:32','ORIG','Galina','Wednesday']]
        
        cols = ['period','student','teacher','dow']
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)
                                         #('dow',"\"Wednesday\""))
        
        self.assertListEqual(expected_result,rows)
        
    def tearDown(self):
        #os.remove(self.tmpdbname+".sqlite")
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")        
        self.ui.destroy()
        
class Test_Insert_Multiple_Rows_onto_Loaded_Rows(unittest.TestCase):
    def setUp(self):
        
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'
        self.dbname = 'test_dbtableviewer'
        self.dbfilename = path.join(dbpath,self.dbname)
        self.ui = DBTableUI()        
        self.ui.dbname_entry_sv.set(self.dbname)
        self.ui.load()
        #self.tmpdbname = path.join(dbpath,'test_tmp')
        #copyfile(dbname+".sqlite",self.tmpdbname+".sqlite")
        self.database = Database(self.dbfilename)    

    def test_insert_row(self):
        
        self.ui.newrowgrid.widgets[1][0].sv.set('Friday')
        self.ui.newrowgrid.widgets[1][1].sv.set('wp')
        self.ui.newrowgrid.widgets[1][2].sv.set('lesson')
        self.ui.newrowgrid.widgets[1][3].sv.set('9:52-10:32')
        self.ui.newrowgrid.widgets[1][4].sv.set('1')
        self.ui.newrowgrid.widgets[1][5].sv.set('1')
        self.ui.newrowgrid.widgets[1][6].sv.set('DAVID')
        self.ui.newrowgrid.widgets[1][7].sv.set('ELA')
        self.ui.newrowgrid.widgets[1][8].sv.set('Brian')
        self.ui.newrowgrid.widgets[1][9].sv.set('9,9,9')
        
        self.ui.newrowgrid.widgets[2][0].sv.set('Friday')
        self.ui.newrowgrid.widgets[2][1].sv.set('wp')
        self.ui.newrowgrid.widgets[2][2].sv.set('lesson')
        self.ui.newrowgrid.widgets[2][3].sv.set('9:52-10:32')
        self.ui.newrowgrid.widgets[2][4].sv.set('1')
        self.ui.newrowgrid.widgets[2][5].sv.set('1')
        self.ui.newrowgrid.widgets[2][6].sv.set('PETER')
        self.ui.newrowgrid.widgets[2][7].sv.set('ELA')
        self.ui.newrowgrid.widgets[2][8].sv.set('Foobar')
        self.ui.newrowgrid.widgets[2][9].sv.set('9,9,9')
        
        self.ui.newrowgrid.widgets[3][0].sv.set('Friday')
        self.ui.newrowgrid.widgets[3][1].sv.set('wp')
        self.ui.newrowgrid.widgets[3][2].sv.set('lesson')
        self.ui.newrowgrid.widgets[3][3].sv.set('9:52-10:32')
        self.ui.newrowgrid.widgets[3][4].sv.set('1')
        self.ui.newrowgrid.widgets[3][5].sv.set('1')
        self.ui.newrowgrid.widgets[3][6].sv.set('PAUL')
        self.ui.newrowgrid.widgets[3][7].sv.set('ELA')
        self.ui.newrowgrid.widgets[3][8].sv.set('Galina')
        self.ui.newrowgrid.widgets[3][9].sv.set('9,9,9')
        
        #self.ui.mainloop()
        
        self.ui.insert(self.database)
        
        expected_result = [['8:30-9:10','COBY','Amelia','Tuesday'],
                           ['9:52-10:32','DAVID','Brian','Friday'],
                           ['9:52-10:32','PETER','Foobar','Friday'],
                           ['9:52-10:32','PAUL','Galina','Friday']]
        
        cols = ['period','student','teacher','dow']
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)
        
        print expected_result,rows
        self.assertListEqual(expected_result,rows)
        
    def tearDown(self):
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")
        #os.remove(self.tmpdbname+".sqlite")
        self.ui.destroy()
        
class Test_Load_Insert_Update_Insert(unittest.TestCase):
    def setUp(self):
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'        
        self.dbname = 'test_dbtableviewer'
        self.dbfilename = path.join(dbpath,self.dbname)
        self.ui = DBTableUI()
        self.ui.dbname_entry_sv.set(self.dbfilename)
        self.ui.load()

        self.database = Database(self.dbfilename)


    def test_insert_row(self):

        self.ui.newrowgrid.widgets[1][0].sv.set('Friday')
        self.ui.newrowgrid.widgets[1][1].sv.set('wp')
        self.ui.newrowgrid.widgets[1][2].sv.set('lesson')
        self.ui.newrowgrid.widgets[1][3].sv.set('9:52-10:32')
        self.ui.newrowgrid.widgets[1][4].sv.set('1')
        self.ui.newrowgrid.widgets[1][5].sv.set('1')
        self.ui.newrowgrid.widgets[1][6].sv.set('DAVID')
        self.ui.newrowgrid.widgets[1][7].sv.set('ELA')
        self.ui.newrowgrid.widgets[1][8].sv.set('Brian')
        self.ui.newrowgrid.widgets[1][9].sv.set('9,9,9')
        
        self.ui.insert(self.database)
        
        self.ui.entrygrid.widgets[2][6].sv.set("FOOBAR")
        self.ui.process_updates(self.database)
        

        self.ui.newrowgrid.widgets[1][0].sv.set('Friday')
        self.ui.newrowgrid.widgets[1][1].sv.set('wp')
        self.ui.newrowgrid.widgets[1][2].sv.set('lesson')
        self.ui.newrowgrid.widgets[1][3].sv.set('9:52-10:32')
        self.ui.newrowgrid.widgets[1][4].sv.set('1')
        self.ui.newrowgrid.widgets[1][5].sv.set('1')
        self.ui.newrowgrid.widgets[1][6].sv.set('PETER')
        self.ui.newrowgrid.widgets[1][7].sv.set('ELA')
        self.ui.newrowgrid.widgets[1][8].sv.set('Foobar')
        self.ui.newrowgrid.widgets[1][9].sv.set('9,6,9')
        
        self.ui.insert(self.database)
        
        expected_results = [['8:30-9:10','COBY','Amelia','Tuesday'],
                            ['9:52-10:32','FOOBAR','Brian','Friday'],
                            ['9:52-10:32','PETER','Foobar','Friday']]
     
        

        cols = ['period','student','teacher','dow']
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)

        print expected_results,rows
        self.assertListEqual(expected_results,rows)
        
    def tearDown(self):
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")
        self.ui.destroy()

class Test_Load_Insert_Update(unittest.TestCase):
    def setUp(self):
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'        
        self.dbname = 'test_dbtableviewer'
        self.dbfilename = path.join(dbpath,self.dbname)
        self.ui = DBTableUI()
        self.ui.dbname_entry_sv.set(self.dbfilename)
        self.ui.load()

        self.database = Database(self.dbfilename)


    def test_insert_row(self):

        self.ui.newrowgrid.widgets[1][0].sv.set('Friday')
        self.ui.newrowgrid.widgets[1][1].sv.set('wp')
        self.ui.newrowgrid.widgets[1][2].sv.set('lesson')
        self.ui.newrowgrid.widgets[1][3].sv.set('9:52-10:32')
        self.ui.newrowgrid.widgets[1][4].sv.set('1')
        self.ui.newrowgrid.widgets[1][5].sv.set('1')
        self.ui.newrowgrid.widgets[1][6].sv.set('DAVID')
        self.ui.newrowgrid.widgets[1][7].sv.set('ELA')
        self.ui.newrowgrid.widgets[1][8].sv.set('Brian')
        self.ui.newrowgrid.widgets[1][9].sv.set('9,9,9')
        
        self.ui.insert(self.database)
        
        self.ui.entrygrid.widgets[2][6].sv.set("FOOBAR")
        
        print self.ui.updates
        #self.ui.process_updates(self.database)         
        
        expected_results = [['8:30-9:10','COBY','Amelia','Tuesday'],
                            ['9:52-10:32','FOOBAR','Brian','Friday']]
     
        cols = ['period','student','teacher','dow']
        
        #print self.ui.entrygrid.dump_grid()
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)

        #print expected_results,rows
        self.assertListEqual(expected_results,rows)
        
    def tearDown(self):
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")
        self.ui.destroy()

        
class Test_Change_Column_of_Loaded_Rows(unittest.TestCase):
    def setUp(self):
        
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'
        self.dbbname = 'test_dbtableviewer'
        self.dbfilename = path.join(dbpath,self.dbbname)
        self.ui = DBTableUI()        
        self.ui.dbname_entry_sv.set(self.dbbname)
        self.ui.load()
        self.database = Database(self.dbfilename)
        self.ui.entrygrid.widgets[0][1].sv.set('foobar')

    def test_update_queue(self):
        
        expected_results =  [('dow',1),('foobar',2),('objtype',1),('period',1),('saveversion',1),('schedule',1),('student',1),('subject',1),('teacher',1),('userobjid',1)]
        
        values,bgcolor = self.ui.updates_get('entrygrid',ignoreaxes=False)

        self.assertListEqual(values[0][:-2], expected_results)

    def test_last_widget_values(self):

        expected_results =  [('dow','dow'),('lessontype','lessontype'),  ('objtype','objtype'), ('period','period'), ('saveversion','saveversion'), ('schedule','schedule'), ('student','student'),('subject','subject'), ('teacher','teacher'),('userobjid','userobjid'),('__timestamp','__timestamp'),('__id','__id')]

        values = self.ui.widget_current_values_get('entrygrid',0)
        
        self.assertListEqual(values, expected_results)

    def test_dbwrite(self):
        
        expected_results_coldefn = ['dow', 'foobar', 'objtype','period', 'saveversion', 'schedule', 'student', 'subject', 'teacher', 'userobjid', '__timestamp', '__id']
        expected_results_rows = ['Tuesday','wp','lesson','8:30-9:10',0,1,'COBY','MATH','Amelia','1,5,4']
        
        self.ui.process_updates(self.database)
        
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson')  
           
        self.assertListEqual(expected_results_rows,rows[0][:-2])
        self.assertListEqual(expected_results_coldefn,colndefn)
        
        
    def tearDown(self):
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")        
        #os.remove(self.tmpdbname+".sqlite")
        self.ui.destroy()
        
        
class Test_Add_Column_of_Loaded_Rows(unittest.TestCase):
    #not using the next free column to see if it works
    
    def setUp(self):
        
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'
        self.dbbname = 'test_dbtableviewer'
        self.dbfilename = path.join(dbpath,self.dbbname)
        self.ui = DBTableUI()        
        self.ui.dbname_entry_sv.set(self.dbbname)
        self.ui.load()
        self.database = Database(self.dbfilename)
        
        self.ui.entrygrid.widgets[0][12].sv.set('foobar')
        
    def test_update_queue(self):
        
        # until save reload column name is actually in 2 places
        expected_results = [('dow',1),('lessontype',1),('objtype',1),('period',1),('saveversion',1),('schedule',1),('student',1),('subject',1),('teacher',1),('userobjid',1),('__timestamp',1),('__id',1),('foobar',1)]
        
        #expected_results = [['', '', '', '', '', '', '', '', '', '', '', '', ('foobar', 0)]]
                
        values,bgcolor = self.ui.updates_get('entrygrid',ignoreaxes=False)

        self.assertListEqual(values[0], expected_results)

    def test_last_widget_values(self):
        
        # ('','') not on the end as blank, blanks get suppressed by current_value_get
        #expected_results =  [('dow','dow'),('','lessontype'),  ('','objtype'), ('','period'), ('','saveversion'), ('','schedule'), ('','student'),('','subject'), ('','teacher'),('','userobjid'),('','__timestamp'),('','__id')]
        expected_results =  [('dow','dow'),('lessontype','lessontype'),  ('objtype','objtype'), ('period','period'), ('saveversion','saveversion'), ('schedule','schedule'), ('student','student'),('subject','subject'), ('teacher','teacher'),('userobjid','userobjid'),('__timestamp','__timestamp'),('__id','__id')]

        values = self.ui.widget_current_values_get('entrygrid',0)

        self.assertListEqual(values, expected_results)

    def test_dbwrite(self):
        
        self.ui.process_updates(self.database)

        expected_results_coldefn = ['dow', 'lessontype', 'objtype', 'period', 'saveversion', 'schedule', 'student', 'subject', 'teacher', 'userobjid', '__timestamp', '__id','foobar']
              
        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson')  
        
        self.assertListEqual(expected_results_coldefn,colndefn)
        
    def tearDown(self):
        #os.remove(self.tmpdbname+".sqlite")
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")                
        self.ui.destroy()
        
class Test_Add_Column_of_Loaded_Rows_With_Values(unittest.TestCase):
    #not using the next free column to see if it works
    
    def setUp(self):
        
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'
        self.dbname = 'test_dbtableviewer'
        self.dbfilename = path.join(dbpath,self.dbname)
        self.ui = DBTableUI()        
        self.ui.dbname_entry_sv.set(self.dbname)
        self.ui.load()
        #self.tmpdbname = path.join(dbpath,'test_tmp')
        #copyfile(dbname+".sqlite",self.tmpdbname+".sqlite")
        #self.database = Database(self.tmpdbname)
        self.database = Database(self.dbfilename)

    def test_change_colname_to_foobar(self):
        
        expected_results_coldefn = ['dow', 'lessontype', 'objtype', 'period', 'saveversion', 'schedule', 'student', 'subject', 'teacher', 'userobjid', '__timestamp', '__id','foobar']
      
        expected_results_rows = [['Tuesday','wp','lesson','8:30-9:10',0,1,'COBY','MATH','Amelia','1,5,4','19:43:01','049C2F17','d']]


        self.ui.entrygrid.widgets[0][17].sv.set('foobar')

        self.ui.entrygrid.widgets[1][17].sv.set('d')

        
        self.ui.process_updates(self.database)
        
        with self.database:
            _,rows = tbl_rows_get(self.database,'lesson')  
        
        self.assertListEqual(expected_results_rows,rows)
        
    def tearDown(self):
        copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")        

        #os.remove(self.tmpdbname+".sqlite")
        self.ui.destroy()
    
class Test_New_DBTable_Insert(unittest.TestCase):
    def setUp(self):
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'        
        self.dbname = 'test_dbtableviewer_tmp'
        self.dbfilename = path.join(dbpath,self.dbname)
        self.ui = DBTableUI()
        self.ui.dbname_entry_sv.set(self.dbfilename)
        #self.ui.load()

        self.database = Database(self.dbfilename)

        self.ui.newrowgrid.widgets[0][0].sv.set('A')
        self.ui.newrowgrid.widgets[0][1].sv.set('B')
        self.ui.newrowgrid.widgets[0][2].sv.set('C')
    
        self.ui.newrowgrid.widgets[1][0].sv.set('1')
        self.ui.newrowgrid.widgets[1][1].sv.set('2')
        self.ui.newrowgrid.widgets[1][2].sv.set('3')

    def test_(self):
      
        #self.ui.mainloop()
        self.ui.insert(self.database)  

        expected_results = [[1,2,3]]
     
        cols = ['A','B','C']

        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)

        self.assertListEqual(expected_results,rows)
        
    def tearDown(self):
        #copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")
        os.remove(self.dbname+".sqlite")
        self.ui.destroy()
        
class Test_New_DBTable_Insert_Change_Save(unittest.TestCase):
    def setUp(self):
        dbpath = '/home/burtnolej/Development/pythonapps3/clean/apps/schoolschedulewizard/'        
        self.dbname = 'test_dbtableviewer_tmp'
        self.dbfilename = path.join(dbpath,self.dbname)
        self.ui = DBTableUI()
        self.ui.dbname_entry_sv.set(self.dbfilename)
        #self.ui.load()

        self.database = Database(self.dbfilename)

        self.ui.newrowgrid.widgets[0][0].sv.set('A')
        self.ui.newrowgrid.widgets[0][1].sv.set('B')
        self.ui.newrowgrid.widgets[0][2].sv.set('C')
    
        self.ui.newrowgrid.widgets[1][0].sv.set('1')
        self.ui.newrowgrid.widgets[1][1].sv.set('2')
        self.ui.newrowgrid.widgets[1][2].sv.set('3')
        
        self.ui.insert(self.database)
        
        self.ui.entrygrid.widgets[1][1].sv.set('foobar')

    '''def test_update_queue(self):
        
        # until save reload column name is actually in 2 places
        expected_results = [[('A',1),('B',1),('C',1)],
                            [('1',1),('foobar',2),('3',1)]]
                            
                
        values,bgcolor = self.ui.updates_get('entrygrid',ignoreaxes=False)

        self.assertListEqual(values[0][:-2], expected_results[0])
        self.assertListEqual(values[1][:-2], expected_results[1])


    def test_last_widget_values(self):
        
        # ('','') not on the end as blank, blanks get suppressed by current_value_get
        #expected_results =  [('dow','dow'),('','lessontype'),  ('','objtype'), ('','period'), ('','saveversion'), ('','schedule'), ('','student'),('','subject'), ('','teacher'),('','userobjid'),('','__timestamp'),('','__id')]
        expected_results_row0 =  [('A','A'),('B','B'),  ('C','C')]
        expected_results_row1 =  [('',1),('',2),  ('',3)]
        
        values = self.ui.widget_current_values_get('entrygrid',0)

        self.assertListEqual(values[:-2], expected_results_row0)
        
        values = self.ui.widget_current_values_get('entrygrid',1)

        self.assertListEqual(values[:-2], expected_results_row1)'''
        
    def test_dbwrite(self):
      
        #self.ui.mainloop()

        self.ui.process_updates(self.database)
        
        expected_results = [[1,'foobar',3]]
     
        cols = ['A','B','C']

        with self.database:
            colndefn,rows = tbl_rows_get(self.database,'lesson',cols)

        self.assertListEqual(expected_results,rows)
        
    def tearDown(self):
        #copyfile(self.dbfilename+".sqlite.backup",self.dbfilename+".sqlite")
        os.remove(self.dbname+".sqlite")
        self.ui.destroy()
        
        

        
if __name__ == "__main__":
    suite = unittest.TestSuite()

    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Grid_Behaviour_Focus))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Grid_Behaviour_Update_Entry))
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Clear_Load))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Change_Save))
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Insert_Save))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Insert_Change_Save))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Load_Insert_Change_Save_Insert_Save))
    
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Change_Column_of_Loaded_Rows))
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_Add_Column_of_Loaded_Rows))
         
    #suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_New_DBTable_Insert))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_New_DBTable_Insert_Change_Save))
    
    

    
    
    
    
    unittest.TextTestRunner(verbosity=2).run(suite) 



