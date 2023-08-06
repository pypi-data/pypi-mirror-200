import sys
sys.path.append("../src/vml_parser")
import vml 
import json

import unittest

class TestVML(unittest.TestCase):
    def test_parse(self):
        with open("test.vml", "r") as f:
            lines = f.readlines()
        
        data = str(vml.parse(lines)).strip()
        
        result = '[{"element 1": [{"things": ["dog", {"snacks": [{"apple": [], "checked":false}, "pear"], "checked":true}, "house"]}, {"names": ["james", "alfred"]}]}, {"element 2": ["foo", "bar", "baz"], "checked":false}, "foobar"]'.strip()
        
        self.assertEqual(data,result)
        
    def test_dump(self):
        element1 = vml.Element("element 1")

        element1.children = [vml.Element("things"), vml.Element("names")]

        element1.children[0].children = [vml.Element("dog"), vml.Element("snacks"), vml.Element("house")]
        element1.children[1].children = [vml.Element("james"), vml.Element("alfred")]

        element1.children[0].children[1].children = [vml.Element("apple"), vml.Element("pear")]

        element1.children[0].children[1].setchecked(True)
        element1.children[0].children[1].children[0].setchecked(False)
        

        element2 = vml.Element("element 2")
        element2.children = [vml.Element("foo"), vml.Element("bar"), vml.Element("baz")]
        
        element2.setchecked(False)
        

        foobar = vml.Element("foobar")
        
        root = [element1, element2, foobar]
        
        dump = vml.dump(root)
        result = ['element 1', '\tthings', '\t\tdog', '\t\t[x] snacks', '\t\t\t[ ] apple', '\t\t\tpear', '\t\thouse', '\tnames', '\t\tjames', '\t\talfred', '[ ] element 2', '\tfoo', '\tbar', '\tbaz', 'foobar']
        
        self.assertEqual(dump, result)
        
    def test_dumps(self):
        with open("test.json", "r") as f:
            lines = f.readlines()
        
        dump = vml.dumps(lines)
        result = ['element 1', '\tthings', '\t\tdog', '\t\t[x] snacks', '\t\t\t[ ] apple', '\t\t\tpear', '\t\thouse', '\tnames', '\t\tjames', '\t\talfred', '[ ] element 2', '\tfoo', '\tbar', '\tbaz', 'foobar']
        
        self.assertEqual(dump, result)
