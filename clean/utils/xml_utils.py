
import xml.etree.ElementTree as xmltree

def element_find_tags(filen, tag, root=None,ns=None):
    ''' starting at the root, search for any elements where tag=tag
    and return a list of those xmlelement objects. root will default
    to the top of the tree unless a lower level node is provided '''
    
    if root==None: #assume we search from actual tree root
        search_root = xmltree.parse(filen)
    else:
        search_root = root
        
    return(search_root.findall(tag,ns))
           
def element_find_children(parent):
    ''' for a given xml element, return all children as a list of tuples of the form
    (name,value)'''
    
    d={}
    for child in parent._children:
        d[child.tag]=child.text
    return(d)

def element_attrib_as_string(element):
    s=""
    for key,value in element.attrib.iteritems():
        s=s+value
    return(s)
    
def element_find_by_attrib_value(root,tag,attrib,attrib_val):
    
    xpath_str = ".//{0}[@{1}='{2}']".format(tag,attrib,attrib_val)
    print xpath_str
    return(root.find(xpath_str))
    

def element_move(root,element,new_parent):
    
    from copy import deepcopy
    parent_map = dict((c, p) for p in root.getiterator() for c in p)

    element_copy = deepcopy(element)
    new_parent.append(element_copy)
    
    old_parent = parent_map[element]
    old_parent.remove(element)
  

def element_fuse(root,element_tag,new_parent):
    
    from copy import deepcopy

    root_copy = deepcopy(root)

    # remove all children from the copy
    # cast to a separate list instance so we get around the
    # 'cant delete from the iterator your iterating with'
    for child in list(root_copy.getchildren()):
        root_copy.remove(child)
        
    # add new element to copy
    new_element =  xmltree.SubElement(root_copy,element_tag)
    
    # get children from orig and copy to new element
    for child in root.getchildren():
        new_element.append(child)
    
    return(root_copy)
    
def element_parent_get(root,element):
    parent_map = dict((c, p) for p in root.getiterator() for c in p)    
    return(parent_map[element])
        
def grid2xml(grid):
    # take a 2d array and return an XML string
    # nodes are called root, row and cell
    # if cell content is a string it will be mapped to text
    # if its a list it will be mapped to subcells
    # if its a dict it will be mapped to sub elements with node names mapped to keys
    
    from types import StringType, ListType, IntType, DictType
    
    root = xmltree.Element('root')
    
    for row in grid:
        rowelement = xmltree.SubElement(root,"row")
        for cell in row:
            cellelement = xmltree.SubElement(rowelement,"cell")
            if isinstance(cell,StringType):
                cellelement.text = cell
            elif isinstance(cell,IntType):
                cellelement.text = str(cell)
            elif isinstance(cell,ListType):
                for _cell in cell:
                    subcellelement = xmltree.SubElement(cellelement,"subcell")
                    subcellelement.text = str(_cell)
            elif isinstance(cell,DictType):
                for k,v in cell.iteritems():
                    subcellelement = xmltree.SubElement(cellelement,k)
                    subcellelement.text = str(v)    
    
    return(root)


def xml2string(root):
    
    return(xmltree.tostring(root))

if __name__ == "__main__":
    pass

       