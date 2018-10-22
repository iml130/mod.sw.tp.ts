__author__ = "Dominik Lux"
__credits__ = ["Peter Detzner"]
__maintainer__ = "Dominik Lux"
__version__ = "0.0.1a"
__status__ = "Developement"

import unittest
from objectFiwareConverter import ObjectFiwareConverter
from ObjectToJson.entity import Entity
from JsonToObject.reverseEntity import ReverseEntity


class Test_JsonConverter(unittest.TestCase):

    def test_2Fiware(self):
        ObjectFiwareConverter.obj2Fiware(TestClass(), ind=4)

    def test_2Obj(self):
        json = """{"type": "TestClass", "id": "TestClass1", "val": {"type": "number", "value": 1, "metadata": {} } }"""
        tc = TestClass()
        tc.val = 2L
        ObjectFiwareConverter.fiware2Obj(json, tc)
        self.assertEqual(tc.val, 1)

    def test_2ObjWithOutMetaData_Unicode(self):
        json = """{"type":"TestClass","id":"ID","val":{"type":"string","value":"i am unicode","metadata":{"python":{"type":"dataType","value":"unicode"}}}}"""
        tc = TestClass()
        tc.val = str(" ")
        ObjectFiwareConverter.fiware2Obj(json, tc, useMetadata=False)
        self.assertEqual(type(tc.val), str)
        self.assertEqual(tc.val, "i am unicode")  # Not unicode

    def test_2ObjWithOutMetaDataAndTypeCheck_Unicode(self):
        json = """{"type":"TestClass","id":"ID","val":{"type":"string","value":"i am unicode","metadata":{"python":{"type":"dataType","value":"unicode"}}}}"""
        tc = TestClass()
        ObjectFiwareConverter.fiware2Obj(
            json, tc, useMetadata=False, ignoreWrongDataType=True)
        self.assertEqual(type(tc.val), str)
        self.assertEqual(tc.val, "i am unicode")  # Not unicode

    def test_2ObjWithOutMetaData_Complex(self):
        json = """{"type": "TestClass","id": "ID","val": 
                 {"type": "array","value": 
                    [{"type": "number","value": 0.0,"metadata": {"python": {"type": "dataType","value": "float"}}},
                     {"type": "number","value": 2.1,"metadata": {"python": {"type": "dataType","value": "float"}}}]
                ,"metadata": {"python": {"type": "dataType","value": "complex"}}}}"""
        tc = TestClass()
        tc.val = list()
        ObjectFiwareConverter.fiware2Obj(json, tc, useMetadata=False)
        self.assertEqual(type(tc.val), list)
        self.assertEqual(tc.val, [0, 2.1])  # Not unicode

    def test_2Fiware2Obj(self):
        json = ObjectFiwareConverter.obj2Fiware(TestClass())

        tc = TestClass()
        tc.val = 42
        ObjectFiwareConverter.fiware2Obj(json, tc)

        self.assertEqual(tc.val, 1)

    def test_IntegerType(self): ### TODO Accept Integers and other primitives?
        json = """{"id":"Task1","type":"Task","task":{"type":"Integer","value":0}}"""
        tc = TestClass()
        tc.val = 1 # set Number/Integer

        ObjectFiwareConverter.fiware2Obj(json, tc, setAttr=True)

        self.assertEqual(getattr(tc, 'task'), 0)
        self.assertEqual(getattr(tc, 'id'), 'Task1')
        self.assertEqual(getattr(tc, 'type'), 'Task')
        self.assertEqual(tc.val, 1)

class TestClass(object):
    def __init__(self):
        self.val = 1
