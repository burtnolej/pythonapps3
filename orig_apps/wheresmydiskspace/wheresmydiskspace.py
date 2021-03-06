from sys import path,stdout,argv
import sys
path.append("/Users/burtnolej/Dev/pythonapps/util")
from filesystem_util import read_file_delim, read_dir, getdirsize,read_dir_iter,relname
from misc_util import Logger
from test_util import run_tests, Tester, test_xml_iter, TestUnexpectedResult
import xml.etree.ElementTree as xmltree
from db_util import Database, DatabaseTable, DatabaseRecord, DatabaseView
from datetime_util import MyDT
from table_print import HashObjectTablePrint

# 0826 0706
# also ObjectPrinter not working
# also need to init git from top level
# also need to try to retrieve backup from time machine of db_test
# in find_changed_records we are not going into ins_batch_list
# i also dont think _iter_records is returning all the records
# figure this out by getting ObjectPrinter to work for a Table

class Filesystem(Database):
    pass

class Ref(DatabaseTable):
    def __init__(self,*args,**kwargs):
        super(Ref,self).__init__(*args,**kwargs)
        self._set_pk("version")

    def ref(self,**kwargs):
        g = Node(**kwargs)
        self[kwargs.__getitem__('version')] = g

class Nodes(DatabaseTable):
    def __init__(self,*args,**kwargs):
        super(Nodes,self).__init__(*args,**kwargs)
        self._set_pk("name")

    def node(self,**kwargs):
        g = Node(**kwargs)
        self[kwargs.__getitem__('name')] = g

class Node(DatabaseRecord):
    pass


class TestGetDirSize(Tester):
    def __init__(self,descr,pos_test,exception,**kw):
        #self.start_path = "./test"
        #self.results = tuple([160000,15,[],True])
        #print self.results

        self.test(descr,pos_test,exception,**kw)
        
    def run(self):
        return(getdirsize(self.start_path))

        #if self.results_actual != self.results:
        #    raise TestUnexpectedResult(self.results_actual)

    
l = Logger('/tmp/log.txt')

#tree = xmltree.parse("./tests.xml")

#for o,arg,fields in test_xml_iter(tree,'test'):
#    clsobj = globals()[o]  # get test class instance
#    _nodes,total_size = clsobj(*arg,**fields)

def create_db(db,secs,_nodes):
    nodes = db.table(Nodes)
    ref = db.table(Ref)
    _ref = [{'version':'current','value':secs},
             {'version':'prev','value':None}]

    nodes.add_list(_nodes)
    ref.add_list(_ref)
    db.init_objects_in_db()

def update_db(db,secs,_nodes):
    nodes = db.table(Nodes)
    ref = db.table(Ref)
    db.init_objects_in_db()
    
    nodes.add_list(_nodes)
    cval = ref.get_rec_field_value('current','value')
    ref.update_rec('prev','value',cval)
    ref.update_rec('current','value',secs)

filesystem = Filesystem("~/gadfly/scripts/","auto")
secs = MyDT.now(display_fmt='%s').value
_nodes,_size = getdirsize(secs,"./0x1dbab")
#_nodes,_size = getdirsize(secs,"/")

### 1950 7714
# current code doesnt handle insert record with an existing pkey correctly
# need to define what it should do in this case (auto update fields that have changed ?) add a new record and make current (need to fix unique key issue)
# also need to add the func to handle a clustered key

if filesystem._type == 'create':
    create_db(filesystem,secs,_nodes)
elif filesystem._type == 'use':
    update_db(filesystem,secs,_nodes)


filesystem.commit_to_gf()
filesystem.close()

filesystem.logmeta.pprint(l.stk_log_handle)

HashObjectTablePrint(filesystem).printout(l.stk_log_handle)
for table in filesystem.values():
    for rec in table:
        table[rec].pprint()
        HashObjectTablePrint(table,_max_column_width=5).printout(l.stk_log_handle)

exit()


#dirname = "/Volumes/Seagate

print "f_size".ljust(11),
print "f_count".ljust(8),
print "parent".ljust(16),
print "file/dir"

dirname = "/Users/burtnolej/Dev/pythonapps/apps/wheresmydiskspace/test"
funcname = getdirsize
depth = 2
size,total_skip = wmds(funcname,dirname,depth)

gb_size = round(size/1024/1024,2)
print dirname,gb_size,str(funcname)
print total_skip

