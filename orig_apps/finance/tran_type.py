#!/usr/bin/python

from sys import path
path.append("/Users/burtnolej/Dev/pythonapps/util")
from misc_util import file2list, switch, pprint_exception
from db_util import DatabaseTable, DatabaseRecord
from operator import mod
from collections import OrderedDict

class TransactionTypes(DatabaseTable):
    def transaction_type(self,**kwargs):
        tran_amt = kwargs['_tran_amt']
        kwargs.pop('_tran_amt')
        if (kwargs['_mangle'].startswith('POS') or kwargs['_mangle'].startswith('2201') or kwargs['_mangle'].startswith('4097')):
            kwargs.__setitem__('_db_name','POS')
        elif kwargs['_mangle'].startswith('CHAPS PAYMENT'):
            kwargs.__setitem__('_db_name','CHAPS')
        elif kwargs['_mangle'].startswith('DIRECT DEBIT'):
            kwargs.__setitem__('_db_name','DIRECT_DEBIT')
        elif kwargs['_mangle'].startswith('BACS PAYMENT'):
            kwargs.__setitem__('_db_name','BACS')
        elif kwargs['_mangle'].startswith('STANDING ORDER'):
            kwargs.__setitem__('_db_name','STANDING_ORDER')
        elif mod(float(tran_amt),float(50)) == 0:
            kwargs.__setitem__('_db_name','ATM')
        else:
            kwargs.__setitem__('_db_name','UNKONOWN')
        tt = TranType(**kwargs)

        key = tt.name # make local copy so visible in print_error
        if not self.has_key(key):
            self[key] = tt # new
            return tt
        return self.__getitem__(key)

class TransactionType(DatabaseRecord):
    pass
