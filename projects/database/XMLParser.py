import unittest
import xml.etree.ElementTree as xmltree
import sys
sys.path.append("/home/burtnolej/Development/pythonapps3/utils")
from misc_utils import write_text_to_file

class XMLCreator():
    
    def __init__(self, root_tag, filen=None, ns=None):
        self.filen = filen
        self.tree = xmltree.Element(root_tag)

    @classmethod
    def table(cls, root_tag,table, filen=None, ns=None):
        self.tree = xmltree.Element(root_tag)
        cls1 = cls.__init__(root_tag,filen,ns)
        return(cls1)
    
    def write(self): 
        write_text_to_file(self.filen,self.tree.dump())

    def dump(self):
        return(xmltree.tostring(self.tree))
        
    def add_child_tag(self,parent,tag):
        return(xmltree.SubElement(parent,tag))
                
    def add_child_element(self,element,child):    
        element.append(child)
    
    def add_attr(self,element,attr,attr_val):
        element.set(attr,attr_val)
    
    def update_element(self,element,text):
        element.text = text
        
    def table2xml(self):
        
        # divide table vertically into 2. left side defines parent tags; right side defines child
        # tags; values and attributes
        
        table = [["_id","_parent","_type","root-food","food-name","food-mfr","food-serving","food-calories"],
                 [1,"","root","#2;id=1","","","",""],
                 [2,1,"food","","Avocado Dip","Sunnydale","29;units=g","total=110,fat=100"],
                 [5,"","root","#6;id=5","","","",""],
                 [6,5,"food","","Bagels New York Style","Thompson","104;units=g","total=t350,fat=35"],
                 [9,"","root","#10;id=9","","","",""],
                 [10,9,"food","","Beef Frankfurter, Quarter Pound","Armitage","115;units=g","total=370,fat=290"]]

        parent_defn = zip(*table)[0:2]
        child_defn = zip(*table)[3:len(table[0])]
        
        # get the number of rows that are to be processed
        num_rows = len(parent_defn[0])
        
        # parent tag defns: column headers must be 'tag' and 'tag_id'
        
        for i in range(1,num_rows):
            # set parent tag
            tag=parent_defn[0][i]
            
            # set attr and attr_val
            attr=parent_defn[1][i]
            attr_val=parent_defn[1][i]
            
            # create element
            element = self.add_child_tag(self.tree,tag)
            
            # add id attribute to the element
            self.add_attr(element,"id",attr_val)
        
        print self.dump()


     
class TestXMLCreator(unittest.TestCase):     

    def test_init_tree(self):
        
        # test parameters
        test_root_tag="nutrition"
        
        # set expected results
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = "<nutrition />"
        
        # execute test
        xmlcreator = XMLCreator(test_root_tag)
        results = xmlcreator.dump()
        
        # assert correctness
        self.assertEquals(results,expected_results)

    def test_add_child_tag(self):
        
        # test parameters
        test_root_tag="nutrition"
        test_child_tag="food"
        
        # set expected results
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = "<nutrition><food /></nutrition>"
        
        # test prep
        xmlcreator = XMLCreator(test_root_tag)
        
        # execute test
        xmlcreator.add_child_tag(xmlcreator.tree,test_child_tag)
        results = xmlcreator.dump()
        
        # assert correctness
        self.assertEquals(results,expected_results)
        
    def test_update_element(self):
        
        # test parameters
        test_root_tag="nutrition"
        test_child_tag="food"
        
        # set expected results
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = "<nutrition><food>foobar</food></nutrition>"
        
        # test prep
        xmlcreator = XMLCreator(test_root_tag)
        xmlelement = xmlcreator.add_child_tag(xmlcreator.tree,test_child_tag)
        
        # execute test
        xmlcreator.update_element(xmlelement,"foobar")
        results = xmlcreator.dump()
        
        # assert correctness
        self.assertEquals(results,expected_results)
        
    def test_add_attr(self):
        
        # test parameters
        test_root_tag="nutrition"
        test_child_tag="food"
        
        # set expected results
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = "<nutrition><food foo=\"bar\" /></nutrition>"
        
        # test prep
        xmlcreator = XMLCreator(test_root_tag)
        xmlelement = xmlcreator.add_child_tag(xmlcreator.tree,test_child_tag)
        
        # execute test
        xmlcreator.add_attr(xmlelement,"foo","bar")
        results = xmlcreator.dump()
        
        # assert correctness
        self.assertEquals(results,expected_results)
        
        
    def test_add_child_element(self):
        
        # test parameters
        test_root_tag="nutrition"
        test_child_tag="food"
        test_new_child_tag="blah"
        test_new_gchild_tag="yeh yeh"
        
        # set expected results
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = "<nutrition><food><blah><yeh yeh /></blah></food></nutrition>"
        
        # test prep
        xmlcreator = XMLCreator(test_root_tag)
        xmlelement = xmlcreator.add_child_tag(xmlcreator.tree,test_child_tag)
        
        xmlchildelement = XMLCreator(test_new_child_tag)
        xmlgchildelement = xmlcreator.add_child_tag(xmlchildelement.tree,test_new_gchild_tag)
        
        # execute test
        xmlcreator.add_child_element(xmlelement,xmlchildelement.tree)
        results = xmlcreator.dump()
        
        # assert correctness
        self.assertEquals(results,expected_results)
        
    def test_table_to_xml(self):
        table = [["tag","tag_id","field_name","field_mfr","field_serving","field_calories"],
                 ["food","0001","Avocado Dip","Sunnydale","units=g;29","total=110,fat=100"]	,		
                 ["food","0002","Bagels New York Style","Thompson","units=g;104","total=350,fat=35"],
                 ["food","0003","Beef Frankfurter, Quarter Pound","Armitage","units=g;115","total=370,fat=290"],
                 ["food","0004","Chicken Pot Pie","Lakeson","units=g;198","total=410,fat=200"]]
        
        xmlcreator = XMLCreator("nutrition")
        xmlcreator.table2xml()

        
        xml = "<nutrition>\
        <food id=\"0001\">\
        <name>Avocado Dip</name>\
        <mfr>Sunnydale</mfr>\
        <serving units=\"g\">29</serving>\
        <calories total=\"110\" fat=\"100\"/>\
        </food><food id=\"0002\">\
        <name>Bagels New York Style</name>\
        <mfr>Thompson</mfr>\
        <serving units=\"g\">104</serving>\
        <calories total=\"300\" fat=\"35\"/>\
        </food><food id=\"0003\">\
        <name>Beef Frankfurter, Quarter Pound</name>\
        <mfr>Armitage</mfr>\
        <serving units=\"g\">115</serving>\
        <calories total=\"370\" fat=\"290\"/>\
        </food><food id=\"0004\">\
        <name>Chicken Pot Pie</name>\
        <mfr>Lakeson</mfr>\
        <serving units=\"g\">198</serving>\
        <calories total=\"410\" fat=\"200\"/>\
        </food>\
        </nutrition>"
        
        

class XMLParser():
    
    def __init__(self,schema, ns=None):
        self.tree = xmltree.parse(schema)
        
    def get_xml_root(self):
        ''' return the root node '''
        return(self.tree)
    
    def get_values(self,tag,ns=None):
        
        values=[]               
        for element in self.tree.iter(tag):
                values.append(element.text) 
            
        return values
    
    def get_elements(self,tag, attr=None,attr_val=None,attr_val_pred=None,ns=None):
        
        elements=[]               
        for element in self.tree.iter(tag):
                elements.append(element) 
            
        return elements
    
    def get_elements_by_attr(self,tag, attr,attr_val,attr_val_pred,ns=None):
        
        elements=[]               
        for element in self.tree.iter(tag):
                if element.attrib.has_key(attr):
                    if getattr(self,attr_val_pred)(int(element.attrib[attr]),int(attr_val)):
                        elements.append(element)
            
        return elements
    
    def get_values_by_attr(self,tag, attr,attr_val,attr_val_pred,ns=None):
        
        values=[]               
        for element in self.tree.iter(tag):
                if element.attrib.has_key(attr):
                    if getattr(self,attr_val_pred)(int(element.attrib[attr]),int(attr_val)):
                        values.append(element.attrib[attr])
            
        return values
    
    # Operator methods
    @staticmethod
    def gtequal(val1,val2):
        if val1 >= val2:
            return True
        return False
    
    @staticmethod
    def ltequal(val1,val2):
        if val1 <= val2:
            return True
        return False
    
    @staticmethod
    def equal(val1,val2):
        if val1 == val2:
            return True
        return False
    
    
    
class TestXMLParser(unittest.TestCase):
    
    ''' only provide literal predicates, no objects; i.e. return any elements where tag=SEARCH_TAG under the branch where tag=PREDICATE_TAG 
    therefore if PRED_TAG exists 3 times and each time has 1 descendent called SEARCH_TAG, then 3 elements will be returned
    
    
    | Test Variables
    ---------------------------------------------------------
    | return     | test cond| type  | searchby | pred_type | namespace |
    ---------------------------------------------------------
    | element(s) | bad tag  | pass  | tag      | n/a       | none      |
    | value(s)   | dupe val | fail  | attr_val | gtequal   | ns        |
    |            |          |       |          | ltequal   |           |
    |            |          |       |          | equal     |           |
    ---------------------------------------------------------
    
    | Test Combinations
    ----------------------------------------------------------------------------------------------------
    | return  | args    |type  | searchby  | pred    | test_name                         | function_under_test
    ----------------------------------------------------------------------------------------------------
    | element |         | pass  | tag      | n/a     | test_get_elements                 | get_elements
    | element |         | fail  | tag      | n/a     | test_get_elements                 | get_elements_fail
    | element | bad tag | pass  | tag      | n/a     | test_get_elements                 | get_elements_fail
    | value   |         | pass  | tag      | n/a     | test_get_values                   | get_values
    | value   |         | fail  | tag      | n/a     | test_get_values_fail              | get_values
    | value   | bad tag | pass  | tag      | n/a     | test_get_values_invalid_tag       | get_values
    | element |         | pass  | attr_val | gtequal | test_get_elements_by_attr_gtequal | get_elements_by_attr
    | element |         | pass  | attr_val | ltequal | test_get_elements_by_attr_ltequal | get_elements_by_attr
    | element |         | pass  | attr_val | equal   | test_get_elements_by_attr_equal   | get_elements_by_attr
    | values  |         | pass  | attr_val | gtequal | test_get_values_by_attr_gtequal   | get_values_by_attr
    |
    |
    ---------------------------------------------------------------------------------------------------- 
    
    | Other Tests
    ----------------------------------------------------------------------------------------------------
    | start_node | return  | type | scope | pred | test_name
    ----------------------------------------------------------------------------------------------------
    | root       | tree    | pass | all   | none | get_tree
    |
    ----------------------------------------------------------------------------------------------------
    '''
    
    def setUp(self):
        self.xmlparser = XMLParser("food.xml")
        
    def test_get_tree(self):
        self.assertIsInstance(self.xmlparser.tree,xmltree.ElementTree)
     
     
    # ----------------------------------------------------------   
    # testing the retreival of elements
    # ----------------------------------------------------------
    
    def test_get_elements(self):
        
        # test parameters
        test_tag="food"
        test_attribute="id"
        
        # set expected results
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = ["0001","0002","0003","0004","0005","0006","0007","0008","0009","0010"]
        
        # execute test
        child_elements = self.xmlparser.get_elements(test_tag)
        
        # build result set that can be asserted
        results = []
        for child_element in child_elements:
            results.append(child_element.attrib[test_attribute])
          
        # assert correctness
        self.assertEquals(results,expected_results)
        
    def test_get_elements_fail(self):
        
        # test parameters
        test_tag="food"
        test_attribute="id"
        
        # set expected results
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = ["0001","0002","0003","0004","0005","0007","0008","0009","0010"]
        
        # execute test
        child_elements = self.xmlparser.get_elements(test_tag)
        
        # build result set that can be asserted
        results = []
        for child_element in child_elements:
            results.append(child_element.attrib[test_attribute])
          
        # assert correctness
        self.assertNotEqual(results,expected_results)
        
    def test_get_elements_invalid_tag(self):
        
        # test parameters
        test_tag="foobar"
        test_attribute="id"
        
        # set expected results
        expected_results = []
        
        # execute test
        elements = self.xmlparser.get_elements(test_tag)
        
        # assert correctness
        self.assertEqual(elements,expected_results)
        
    def test_get_elements_by_attr_gtequal(self):
        
        # test parameters
        test_tag="calories"
        test_attr="total"
        test_attr_val="300"
        test_attr_val_pred="gtequal"
        
        # set expected results: the number of elements returned 
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = ["300","370","410"]
        
        # execute test
        elements = self.xmlparser.get_elements_by_attr(test_tag,test_attr,test_attr_val,test_attr_val_pred)
        
        # build result set that can be asserted
        results = []
        for element in elements:
            results.append(element.attrib[test_attr])
            
        # assert correctness
        self.assertEquals(results,expected_results)
        
    def test_get_elements_by_attr_ltequal(self):
        
        # test parameters
        test_tag="calories"
        test_attr="total"
        test_attr_val="300"
        test_attr_val_pred="ltequal"
        
        # set expected results: the number of elements returned 
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = ["110","300","20","70","200","150","160","220"]
        
        # execute test
        elements = self.xmlparser.get_elements_by_attr(test_tag,test_attr,test_attr_val,test_attr_val_pred)
        
        # build result set that can be asserted
        results = []
        for element in elements:
            results.append(element.attrib[test_attr])
            
        # assert correctness
        self.assertEquals(results,expected_results)
        
    def test_get_elements_by_attr_equal(self):
        
        # test parameters
        test_tag="calories"
        test_attr="total"
        test_attr_val="70"
        test_attr_val_pred="equal"
        
        # set expected results: the number of elements returned 
        # actual results will be elements(objects) and so an extra step is needed to compare  
        # attributes on those elements; we compare attributes as tags are not unique
        expected_results = ["70"]
        
        # execute test
        elements = self.xmlparser.get_elements_by_attr(test_tag,test_attr,test_attr_val,test_attr_val_pred)
        
        # build result set that can be asserted
        results = []
        for element in elements:
            results.append(element.attrib[test_attr])
            
        # assert correctness
        self.assertEquals(results,expected_results)
        
        
    
    # ----------------------------------------------------------
    # testing the retreival of values
    # ----------------------------------------------------------
    
    def test_get_values(self):
        
        # test parameters
        test_tag="name"
        
        # set expected results
        expected_results = ["Avocado Dip","Bagels New York Style","Beef Frankfurter, Quarter Pound","Chicken Pot Pie","Cole Slaw","Eggs","Hazelnut Spread","Potato Chips","Soy Patties, Grilled","Truffles, Dark Chocolate"]
        
        # execute test
        values = self.xmlparser.get_values(test_tag)
        
        # assert correctness
        self.assertEquals(values,expected_results)
        
    def test_get_values_fail(self):
        
        # test parameters
        test_tag="name"
        
        # set expected results
        expected_results = ["Avocado Dip","Beef Frankfurter, Quarter Pound","Bagels New York Style","Chicken Pot Pie","Cole Slaw","Eggs","Hazelnut Spread","Potato Chips","Soy Patties, Grilled","Truffles, Dark Chocolate"]
        
        # execute test
        values = self.xmlparser.get_values(test_tag)
        
        # assert correctness
        self.assertNotEqual(values,expected_results)
        
    def test_get_values_invalid_tag(self):
        
        # test parameters
        test_tag="foobar"
        test_attribute="id"
        
        # set expected results
        expected_results = []
        
        # execute test
        elements = self.xmlparser.get_values(test_tag)
        
        # assert correctness
        self.assertEqual(elements,expected_results)
        
    def test_get_values_by_attr_gtequal(self):
        
        # test parameters
        test_tag="calories"
        test_attr="total"
        test_attr_val="300"
        test_attr_val_pred="gtequal"
        
        # set expected results: the number of elements returned 
        expected_results = ["300","370","410"]
        
        # execute test
        values = self.xmlparser.get_values_by_attr(test_tag,test_attr,test_attr_val,test_attr_val_pred)
            
        # assert correctness
        self.assertEquals(values,expected_results)
    
if __name__ == "__main__":
    

    suite = unittest.TestSuite()
    '''
    suite.addTest(TestXMLParser("test_get_elements"))
    suite.addTest(TestXMLParser("test_get_elements_fail"))
    suite.addTest(TestXMLParser("test_get_elements_invalid_tag"))
    suite.addTest(TestXMLParser("test_get_elements_by_attr_gtequal"))
    suite.addTest(TestXMLParser("test_get_elements_by_attr_ltequal"))
    suite.addTest(TestXMLParser("test_get_elements_by_attr_equal"))
    suite.addTest(TestXMLParser("test_get_values"))
    suite.addTest(TestXMLParser("test_get_values_fail"))    
    suite.addTest(TestXMLParser("test_get_values_invalid_tag"))    
    suite.addTest(TestXMLParser("test_get_values_by_attr_gtequal"))  

    
    suite.addTest(TestXMLCreator("test_init_tree")) 
    suite.addTest(TestXMLCreator("test_add_child_tag")) 
    suite.addTest(TestXMLCreator("test_update_element"))
    suite.addTest(TestXMLCreator("test_add_attr"))
    suite.addTest(TestXMLCreator("test_add_child_element"))
    '''

    suite.addTest(TestXMLCreator("test_table_to_xml"))
    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(suite)    