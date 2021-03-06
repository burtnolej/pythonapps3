#!/usr/bin/python

from sys import path
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import file2list, switch, pprint_exception
from db_util import DatabaseTable, DatabaseRecord
from operator import mod
from collections import OrderedDict

class Counterpartys(DatabaseTable):
    def add(self,**kwargs):
        '''
        only add counterparty to collection if it doesnt already exist
        return counterparty object
        '''
        tran_amt = kwargs['_tran_amt']
        kwargs.pop('_tran_amt')
        if kwargs['_mangle'].startswith('POS'):
            c = Counterparty.pos(**kwargs)
        elif kwargs['_mangle'].startswith('2201'):
            c = Counterparty.twotwo(**kwargs)
        elif kwargs['_mangle'].startswith('4097'):
            c = Counterparty.twotwo(**kwargs)
        elif kwargs['_mangle'].startswith('CHAPS PAYMENT'):
            c = Counterparty.chaps(**kwargs)
        elif kwargs['_mangle'].startswith('DIRECT DEBIT'):
            c = Counterparty.directd(**kwargs)
        elif kwargs['_mangle'].startswith('BACS PAYMENT'):
            c = Counterparty.directd(**kwargs)
        elif kwargs['_mangle'].startswith('STANDING ORDER'):
            c = Counterparty.directd(**kwargs)
        #elif www
        elif mod(float(tran_amt),float(50)) == 0:
            c = Counterparty.atm(**kwargs)
        else:
            c = Counterparty.old(**kwargs)
            #raise Exception('cannot proc' + kwargs['_mangle'])

        results = [el for el in sorted(self.keys()) if el[0:4] == c.c_name[0:4]]

        if len(results) == 0:
            key = c.c_name # make local copy so visible in print_error
            self[key] = c # new
            #self.print_status("added",c,c.c_name)
        elif len(results) == 1:
            c = self[results[0]] # exists
            #self.print_status("exists",c,c.c_name)
        else:
            raise Exception("multiple matches for " + key)
        return(c)
    
class Counterparty(DatabaseRecord):
    @classmethod
    def pos(cls,**kwargs):
        assert kwargs.has_key('_mangle')
        cms= kwargs['_mangle'].split() # create a list of words
        c_name = cms[2]
        if len(c_name) < 6:
            c_name = c_name + " " + cms[3][0:6]
        kwargs.__setitem__('c_name',"".join(c_name.split())) # take the spaces out
        c = cls(**kwargs)
        return(c)

    @classmethod
    def twotwo(cls,**kwargs):
        assert kwargs.has_key('_mangle')
        cms = kwargs['_mangle'].split() # create a list of words
        c_name = cms[1][7:][0:10]
        if len(c_name) < 6:
            c_name = c_name + " " + cms[2][0:6]
            if len(c_name) < 10 and len(cms) > 3:
                c_name = c_name + " " + cms[3][0:6]
        kwargs.__setitem__('c_name',"".join(c_name.split())) # take the spaces out
        c = cls(**kwargs)
        return(c)

    @classmethod
    def chaps(cls,**kwargs):
        assert kwargs.has_key('_mangle')
        cms = kwargs['_mangle'].split() # create a list of words
        c_name = "".join(cms[4:6])
        kwargs.__setitem__('c_name',"".join(c_name.split())) # take the spaces out
        c = cls(**kwargs)
        return(c)

    @classmethod
    def directd(cls,**kwargs):
        assert kwargs.has_key('_mangle')
        cms = kwargs['_mangle'].split() # create a list of words
        c_name = "".join(cms[3:5])
        kwargs.__setitem__('c_name',"".join(c_name.split())) # take the spaces out
        c = cls(**kwargs)
        return(c)

    @classmethod
    def atm(cls,**kwargs):
        assert kwargs.has_key('_mangle')
        c_name = kwargs['_mangle'][0:10]
        kwargs.__setitem__('c_name',"".join(c_name.split())) # take the spaces out
        c = cls(**kwargs)
        return(c)

    @classmethod
    def old(cls,**kwargs):
        assert kwargs.has_key('_mangle')
        cms = kwargs['_mangle'].split() # create a list of words
        c_name = "".join(cms[0:2])
        if len(c_name) > 10:
            c_name = "".join(cms[0:1])
        kwargs.__setitem__('c_name',"".join(c_name.split())) # take the spaces out
        c = cls(**kwargs)
        return(c)
