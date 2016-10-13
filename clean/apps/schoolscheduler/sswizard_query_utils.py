import sys
from misc_utils_log import Log, logger
log = Log(cacheflag=True,logdir="/tmp/log",verbosity=10,
          pidlogname=True,proclogname=False)

from database_util import Database, tbl_create
from database_table_util import dbtblgeneric, tbl_rows_get, tbl_query

from sqlite3 import OperationalError

__all__ = ['_execfunc','_rowheaderexecfunc','_columnheaderexecfunc','_dowexecfunc']

def _dowexecfunc(database,value,prep,*args):
    exec_str = "select code from dow "
    return(tbl_query(database,exec_str))

def _colorexecfunc(database,value):
    exec_str = "select rgb from {0} ".format(value)
    return(tbl_query(database,exec_str))

def _sessionenum(database,code,period,prep):
    exec_str = "select enum from session where code = {0} ".format(code)
    exec_str += " and period = {0} ".format(period)
    exec_str += " and prep = {0} ".format(prep)
    return(tbl_query(database,exec_str))

def _maxlessonenum(database):
    exec_str = "select max(enum) from lesson"
    try:
        return tbl_query(database,exec_str)
    except OperationalError:
        return [None,[[0]],None]
    
def _maxsessionenum(database):
    exec_str = "select max(enum) from session"
    try:
        return tbl_query(database,exec_str)
    except OperationalError:
        return [None,[[0]],None]

def _distinct(database,value,table):
    exec_str = "select distinct({1}) from {0} order by prep".format(table,value)
    return tbl_query(database,exec_str)

def _execfunc(database,value,prep,dow):
    exec_str = "select s.code "
    exec_str += "from session as s,adult as a "
    #exec_str += "where a.prep = {0} and ".format(prep)
    exec_str += "where s.prep = {0} and ".format(prep)
    exec_str += "a.name = s.teacher and "
    exec_str += "s.period = {0} and ".format(value)
    #exec_str += "s.day = \"{0}\"".format(dow)
    exec_str += "s.dow = \"{0}\"".format(dow)
    
    return(tbl_query(database,exec_str))

def _rowheaderexecfunc(database):
    exec_str = "select name from period"
    return(tbl_query(database,exec_str))

def _columnheaderexecfunc(database,pred=None,predvalue=None):
    exec_str = "select name from student"
    if pred <> None:
        exec_str = exec_str + " where {0} = {1}".format(pred,predvalue)
    return(tbl_query(database,exec_str))

def _pivotexecfunc(database,title,ycoltype,xcoltype,tblname,whereclause=None,result="count(*)"):
    
    headers = {}
    with database:
        for hdrtype in [ycoltype,xcoltype]:        
            #_,headers[hdrtype],_ =  tbl_query(database,"select distinct({0}) from {1}".format(hdrtype,tblname))
            _,headers[hdrtype],_ =  tbl_query(database,"select name from {0}".format(hdrtype))
            headers[hdrtype] = [_hdrtype[0] for _hdrtype in headers[hdrtype]]

    headers['dow'] = ['MO','TU','WE','TH','FR']

    resulttable = []
    resulttable.append([title] + headers[ycoltype])
    with database:
        for xaxishdr in headers[xcoltype]:
            row=[]
            row.append(xaxishdr)
            for yaxishdr in headers[ycoltype]:
                exec_str = "select {1} from {0} ".format(tblname,result)
                #exec_str = "select subject,teacher from {0} ".format(tblname)
                exec_str += "where {1} = {0} ".format("\""+str(yaxishdr)+"\"",ycoltype)
                exec_str += " and {1} = {0} ".format("\""+str(xaxishdr)+"\"",xcoltype) 
                
                if whereclause <> None:
                    for pred,op,predval in whereclause:
                        exec_str += " and {0} {1} {2} ".format(pred,op,"\""+str(predval)+"\"")
                
                _,results,_ = tbl_query(database,exec_str)
                try:
                    row.append(",".join(results[0]))
                    pass
                except:
                    row.append(0)
            resulttable.append(row)
            
    row=[title]      
    with database:
        for yaxishdr in headers[ycoltype]:
            exec_str = "select count(*) from {0} ".format(tblname)
            exec_str += "where {1} = {0} ".format("\""+str(yaxishdr)+"\"",ycoltype)                
            
            _,results,_ = tbl_query(database,exec_str)
            try:
                row.append(results[0][0])
            except:
                row.append(0)
    resulttable.append(row)
    
    return resulttable

if __name__ == "__main__":
    
    from pprint import pprint
    
    database = Database('quad_new')
    
    with database:
        #_,students,_ = _distinct(database,"name","student")
        _,adults,_ = _distinct(database,"name","adult")
    
    #for student in students:
    for adult in adults:
        print
        print
        
        #results = _pivotexecfunc(database,student[0],'dow','period','lesson',[['student','=',student[0]]],"subject,teacher")
        results = _pivotexecfunc(database,adult[0],'dow','period','lesson',[['teacher','=',adult[0]]],"student")

        for i in range(len(results)-1):
            row=[]
            for item in results[i]:
                row.append(str(item))
            print "^".join(row)
            
        