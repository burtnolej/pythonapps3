#!/usr/bin/python

from sys import path,stdout
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import Singleton, get_time_hms, in_method_log, Logger, file2list
from ui_util import ListBox,EntryBox,TextBox,WindowManager,DocBox,Window,DebugBox
from db_util import Database, DatabaseTable, DatabaseRecord, DatabaseView
from error_util import Notification
from stack_util import get_exception_info
from procs import q_ncd as proc_get_note_create_dates, q_nti as proc_get_note_details, q_nt as proc_get_note_tags, q_nc as proc_get_note_content, u_n_c as proc_update_note_content
import re

import thread_util 
import curses
import time

class NotesDB(Database):
    pass

notesdb = NotesDB("~/Downloads/gadflyZip/gadfly/scripts/",'use')       

def main(screen):
    try:    
        screen.keypad(1)
        curses.mousemask(1)
        curses.nonl()
    
        cdv = notesdb.view(CreateDatesView)
        tv = notesdb.view(TagsView)
        ntv = notesdb.view(NoteTitlesView)
        nt = notesdb.table(NoteTable())
    
        notesdb.loadviews()

        wm = WindowManager()
        cdlb = CreateDatesLB.dbitems(wm,"cdlb",15,15,5,5,cdv)
        cdlb.daemon = True
        cdlb.start()
        cdlb.parent = None
        cdlb.name = "cdlb"

        tvlb = TagsViewLB.dbitems(wm,"tvlb",15,15,5,23,tv)
        tvlb.daemon = True
        tvlb.start()
        tvlb.parent = "cdlb"
        tvlb.name = "tvlb"

        ntvlb = NoteTitlesViewLB.dbitems(wm,"ntvlb",15,60,5,41,ntv)
        ntvlb.daemon = True
        ntvlb.start()
        ntvlb.parent = "ntlb"
        ntvlb.name = "ntvlb"
        
        ntdb = NoteTableDB.blank(wm,"nvdb",15,106,23,5,nt)
        ntdb.daemon = True
        ntdb.start()
        ntdb.parent = "cdlb"
        ntdb.name = "ntdb"

        #eb = CounterpartyNamesFilterEB(wm,"eb1",3,30,32,10)
        #eb.daemon = True
        #eb.start()
        #eb.parent = "lb1"
        #eb.name = "eb1"

        #db = DebugBox(wm,"db",10,50,26,5,True)
        #db.daemon = True
        #db.start()
        #db.name = "db"

        wm.mainloop()
    except KeyboardInterrupt:
        print "Got KeyboardInterrupt exception. Exiting..."
        exit()
    except AssertionError:
        e = get_exception_info()
        Notification.enrich(e['value'])
        exit()
    except:
        e = get_exception_info()
        
        Notification.enrich(e['value'])
        exit()
    finally:
        Notification.print_summary()

class CreateDatesLB(ListBox):
    def context_event_handler(self,event):
        if event in [curses.KEY_DOWN,curses.KEY_UP]:
            (text,_,_,_) = tuple(self._items_sel())
            qm = thread_util.QueueMessage("tvlb",sender=self.name,payload=text)
            with thread_util.threadLock:
                thread_util.MyThread.myQueue.put(qm)

        return False # as we want the super to also process the event

    def run(self):
        while 1:
            #thread_util.MyThread.check_q_exec(self.name,self._filter_dbitems)            
            time.sleep(0.1)

class CreateDatesView(DatabaseView):
    def init_load(self,arg=None,re=None):
        for col1 in proc_get_note_create_dates('create'):
            self.add(create_date = str(col1),display_text=str(col1))
        
    def add(self,**kwargs):
        dr = DatabaseRecord(**kwargs)
        self[dr.create_date] = dr

class TagsViewLB(ListBox):
    def context_event_handler(self,event):
        if event in [curses.KEY_DOWN,curses.KEY_UP]:
            (text,_,_,_) = tuple(self._items_sel())
            qm = thread_util.QueueMessage("ntvlb",sender=self.name,payload=text)
            with thread_util.threadLock:
                thread_util.MyThread.myQueue.put(qm)
        return False # as we want the super to also process the event

    def run(self):
        while 1:
            thread_util.MyThread.check_q_exec(self.name,self._reload_dbitems)            
            time.sleep(0.1)

class TagsView(DatabaseView):
    def init_load(self,arg=None,re=None):
        self.clear()
        for col1 in proc_get_note_tags(arg):
            self.add(tag_name = str(col1),display_text=str(col1))
                
    def add(self,**kwargs):
        dr = DatabaseRecord(**kwargs)
        self[dr.tag_name] = dr

class NoteTitlesViewLB(ListBox):
    def context_event_handler(self,event):
        (text,_,_,rec) = tuple(self._items_sel())
        if event in [curses.KEY_DOWN,curses.KEY_UP]:
            qm = thread_util.QueueMessage("ntdb",sender=self.name,payload=rec)
            with thread_util.threadLock:
                thread_util.MyThread.myQueue.put(qm)

    def run(self):
        while 1:
            thread_util.MyThread.check_q_exec(self.name,self._reload_dbitems)            
            time.sleep(0.1)

class NoteTitlesView(DatabaseView):
    def init_load(self,arg=None,re=None):
        self.clear()
        #for col1 in proc_get_note_titles():
        for col1,col2 in proc_get_note_details():
            self.add(note_title = str(col1),
                     display_text=str(col1),
                     note_id=str(col2))
        
    def add(self,**kwargs):
        dr = DatabaseRecord(**kwargs)
        self[dr.note_title] = dr

class NoteTagsTable(DatabaseTable):
    pass

class NoteTable(DatabaseTable):
    pass

class TagsTable(DatabaseTable):
    pass

class NoteTableDB(DocBox):
    '''
    edit notes, add new notes. add new tags and new notetags if
    needed
    '''
    #def __init__(self,*args):
    #    super(NoteTableDB,self).__init__(*args)
    #    self._note_table = self._dbview # renaming for sake of clarity
        #self._notetags_table =
        #self._tags_table
        
        
    def run(self):
        self._note_title = None # note_title is seed for NoteView
        while 1:
            # store the payload to use in db update statements
            rec = thread_util.MyThread.check_q(self.name)
            if rec :
                self._note_title = rec.note_title
                self._note_id = rec.note_id
                self._dbrec = rec
                self._reload_dbitems(self._note_title) # reload
            time.sleep(0.1)

    def save_item(self):
        # make this a table not a view
        # update the rec view db_util here rather than sp
        proc_update_note_content(self._doc,self._note_title)
        #_db_rec._content = self._doc

        print "the noteid is",self._note_id

        m = re.compile(r"__\w+")
        print "these tags", m.findall(self._doc)

        # get a view with all tags
        #tt = notesdb.table(TagsTable)
        #notedb.load(tt)
        #tt.find(tag_name)
        #tt.add(tag_name)
        #tt.update

        # get a view object for note tags 
        #ntt = notesdb.table(NoteTagsTable)
        #ntt.load(tt)
        #ntv.add(note_id  =,
        #       tag_id = =str(col1))


class NoteTable(DatabaseTable):
    ## what does init_load do for a table?
    ## how does a window on a table update itself
    ## prob only done this for views so far
    ## put a tag on records that show if from db or not
    ## default constructor needs to load whats in db already
    ## tables are straight maps to db so lookups can be done in mem
    def init_load(self,arg=None,re=None):
        self.clear()

        self._note_title = arg
        if arg:
            for col1 in proc_get_note_content(arg):
                self.add(note_content = str(col1),
                         note_title = arg,
                         display_text=str(col1))
        
    def add(self,**kwargs):
        dr = DatabaseRecord(**kwargs)
        self[dr.note_content] = dr


logger = Logger("/tmp/log.txt")
curses.wrapper(main)
logger.__del__()
