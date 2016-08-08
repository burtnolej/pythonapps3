import sys
import os
from os import path as ospath
sys.path.append("/home/burtnolej/Development/pythonapps/clean/utils")
from misc_utils_generic import GenericBase

import unittest
import time

class Test_generic_basic(unittest.TestCase):
    ''' basic operation, pass in dynamic attributes but not flagged
    as data members'''
    def setUp(self):
        self.g = GenericBase(attr1=123,attr2=456)
    
    def tearDown(self):
        pass
        
    def test_construct(self):
        self.assertTrue(hasattr(self.g,'attr1'))
        self.assertEquals(123,getattr(self.g,'attr1'))
        self.assertTrue(hasattr(self.g,'attr2'))
        self.assertEquals(456,getattr(self.g,'attr2'))            

class Test_generic_datamembers(unittest.TestCase):
    ''' using the datamembers constructor to set special attributes 
    ; using the attr_get_keyval method will strip of the _dm_ mangle that is applied to keep them separate '''
    def setUp(self):
        dm = {'foo':'bar','boo':'hah'}
        self.dmg = GenericBase.datamembers(dm)
    
    def tearDown(self):
        pass
    
    def test_hasattr_foo(self):
        self.assertTrue(hasattr(self.dmg,'_dm_foo'))
        
    def test_getattr_foo_bar(self):        
        self.assertEquals('bar',getattr(self.dmg,'_dm_foo')) 

    def test_hasattr_boo(self):
        self.assertTrue(hasattr(self.dmg,'_dm_boo'))
        
    def test_getattr_fboo_hah(self):        
        self.assertEquals('hah',getattr(self.dmg,'_dm_boo')) 

class Test_generic_basic_and_datamembers(unittest.TestCase):
    ''' object with dm attrs and non-dm attrs; using the attr_get_keyval 
    method will strip of the _dm_ mangle that is applied to keep them separate '''
    def setUp(self):
        dm = {'foo':'bar','boo':'hah'}
        self.dmg = GenericBase.datamembers(dm,attr1=123,attr2=456)
    
    def tearDown(self):
        pass
    
    def test_hasattr_foo(self):
        self.assertTrue(hasattr(self.dmg,'_dm_foo'))
        
    def test_getattr_foo_bar(self):        
        self.assertEquals('bar',getattr(self.dmg,'_dm_foo')) 

    def test_hasattr_boo(self):
        self.assertTrue(hasattr(self.dmg,'_dm_boo'))
        
    def test_getattr_fboo_hah(self):        
        self.assertEquals('hah',getattr(self.dmg,'_dm_boo')) 

    def test_hasattr_attr1(self):
        self.assertTrue(hasattr(self.dmg,'attr1'))
        
    def test_getattr_attr1_123(self):        
        self.assertEquals(123,getattr(self.dmg,'attr1')) 
        
    def test_hasattr_attr2(self):
        self.assertTrue(hasattr(self.dmg,'attr2'))
        
    def test_getattr_attr2_456(self):        
        self.assertEquals(456,getattr(self.dmg,'attr2'))  

class Test_generic_datamembers_errors(unittest.TestCase):
    ''' make sure usual errors are detected and caught'''
    def testarg_not_dict(self):
        dm = [('foo','bar'),('boo','hah')]
        
        with self.assertRaises(Exception):
            GenericBase.datamembers(dm)
            
    def testarg_conflicts_with_regular_arg(self):
        dm = {'foo':'bar','boo':'hah'}
        with self.assertRaises(Exception):
            GenericBase.datamembers(dm,foo='bar')
            
class Test_generic_attr_get(unittest.TestCase):
    ''' get  callable and non-callable attrs
    using the attr_get_keyval method will strip of the _dm_ mangle
    that is applied to keep them separate '''
    def setUp(self):
        dm = {'foo':'bar','boo':'hah'}
        self.dmg = GenericBase.datamembers(dm,attr1=123,attr2=456)

    def test_attr_get(self):
        exp_res = ['_setattr','attr_get_keyval','datamembers',
                   'foo','boo','attr1','attr2']
        
        exp_res.sort()
        
        _attr = [_key for _key,_val in self.dmg.attr_get_keyval()]
        _attr.sort()
        
        self.assertListEqual(exp_res,_attr)
        
    def test_attr_exclude_callable(self):
        exp_res = ['foo','boo','attr1','attr2']
        
        exp_res.sort()
        
        _attr = [_key for _key,_val in self.dmg.attr_get_keyval(include_callable=False)]
        _attr.sort()
        
        self.assertListEqual(exp_res,_attr)
        
    def test_attr_get_datamembers(self):
        exp_res = ['foo','boo']
        
        exp_res.sort()
        
        _attr = [_key for _key,_val in self.dmg.attr_get_keyval(include_callable=False,
                                                                include_nondataattr=False)]
        _attr.sort()
        
        self.assertListEqual(exp_res,_attr)


class Test_generic_attr_get_from_derived(unittest.TestCase):
    ''' test that we can distinguish between a base class attribute 
    and a derived class attribute '''
    def setUp(self):
        class DerivedGenericBase(GenericBase):
            staticattr = "imstatic"
            
        dm = {'foo':'bar','boo':'hah'}
        self.dmg = DerivedGenericBase.datamembers(dm,attr1=123,attr2=456)        
        
    def test_attr_get_from_derived_class_only(self):
        _attr = [_key for _key,_val in self.dmg.attr_get_keyval(include_callable=False)]
        _attr.sort()
        
        exp_res = ['foo','boo','attr1','attr2']
        
        exp_res.sort()
        
        _attr = [_key for _key,_val in self.dmg.attr_get_keyval(include_callable=False,
                                                                include_baseattr=False)]
        _attr.sort()
        
        self.assertListEqual(exp_res,_attr)

        
    
if __name__ == "__main__":

    suite = unittest.TestSuite()
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic_basic))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic_datamembers))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic_basic_and_datamembers))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic_datamembers_errors))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic_attr_get))
    suite.addTest(unittest.TestLoader().loadTestsFromTestCase(Test_generic_attr_get_from_derived))

    
    unittest.TextTestRunner(verbosity=2).run(suite)
        
