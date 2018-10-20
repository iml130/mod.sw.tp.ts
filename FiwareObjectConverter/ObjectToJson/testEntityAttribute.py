__author__ = "Dominik Lux"
__credits__ = ["Peter Detzner"]
__maintainer__ = "Dominik Lux"
__version__ = "0.0.1a"
__status__ = "Developement"

import unittest
import json
from entityAttribute import EntityAttribute as EA
from entity import Entity


class TestEntityAttribute(unittest.TestCase):

    def test_EntityAttributeCompletely(self):
        # General functionality given.
        entity = Entity()
        entity.setObject(ComplexExample())
        ComplexExample().ToJSON(entity)
        # No Error thrown

    def test_EntityAttributeBool(self):
        ea = EA(True)
        self.assertEqual(ea.metadata, {})
        self.assertEqual(ea.value, True)
        self.assertEqual(ea.type, "boolean")

        ea = EA(False)
        self.assertEqual(ea.metadata, {})
        self.assertEqual(ea.value, False)
        self.assertEqual(ea.type, "boolean")

    def test_EntityAttributeInt(self):
        ea = EA(1)
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="int")))
        self.assertEqual(ea.value, 1)
        self.assertEqual(ea.type, "number")

    def test_EntityAttributeFloat(self):
        ea = EA(2.132)
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="float")))
        self.assertEqual(ea.value, 2.132)
        self.assertEqual(ea.type, "number")

    def test_EntityAttributeLong(self):
        ea = EA(42L)
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="long")))
        self.assertEqual(ea.value, 42L)
        self.assertEqual(ea.type, "number")

    def test_EntityAttributeComplex(self):
        ea = EA(complex(3, 1))
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="complex")))
        self.assertEqual(ea.value[0].value, 3)
        self.assertEqual(ea.value[1].value, 1)
        self.assertEqual(ea.type, "array")

        ea = EA(2.34j)
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="complex")))
        self.assertEqual(ea.value[0].value, 0)
        self.assertEqual(ea.value[1].value, 2.34)
        self.assertEqual(ea.type, "array")

    def test_EntityAttributeString(self):
        ea = EA("Hello world!")
        self.assertEqual(ea.metadata, {})
        self.assertEqual(ea.value, "Hello world!")
        self.assertEqual(ea.type, "string")

    def test_EntityAttributeUnicode(self):
        ea = EA(u'Unicode')
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="unicode")))
        self.assertEqual(ea.value, u'Unicode')
        self.assertEqual(ea.type, "string")

    def test_EntityAttributeTuple(self):
        ea = EA((1, 2))
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="tuple")))
        self.assertTrue(isinstance(ea.value, list))
        self.assertEqual(ea.value[0].value, 1)
        self.assertEqual(ea.value[1].value, 2)
        self.assertEqual(ea.type, "array")

    def test_EntityAttributeList(self):
        ea = EA([1, 2])
        self.assertEqual(ea.metadata, {})
        self.assertTrue(isinstance(ea.value, list))
        self.assertEqual(ea.value[0].value, 1)
        self.assertEqual(ea.value[1].value, 2)
        self.assertEqual(ea.type, "array")

    def test_EntityAttributeDict(self):
        ea = EA(dict(a=1, b=2))
        self.assertEqual(ea.metadata, {})
        self.assertTrue(isinstance(ea.value, dict))
        self.assertEqual(ea.value.get('a').value, 1)
        self.assertEqual(ea.value.get('b').value, 2)
        self.assertEqual(ea.type, "object")

    def test_EntityAttributeForeignClass(self):
        ea = EA(ClassInt())
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="class")))
        self.assertEqual(ea.type, "ClassInt")
        self.assertTrue(ea.value != None)


# Simple classes for Testing
class SuperEnum(object):
    """ Simple SuperEnum to create Enum-classes
    """
    class __metaclass__(type):
        def __iter__(self):
            for item in self.__dict__:
                if item == self.__dict__[item]:
                    yield item


class Color(SuperEnum):
    """ Simple Enum with different types 
    """
    red = 1
    green = "2"
    blue = 3.12


class ComplexExample(object):
    def __init__(self):
        self.testNone = None
        self.testBool = True
        self.testInt = 42
        self.testFloat = 1.234
        self.testComplex = 42.42j
        self.testStr = 'I am a String'
        self.testUnicode = u'I am Unicode'
        self.testTuple = (43, 2.345, ("Tuple", u' in tuple'))
        self.testList = [44, 3.456, ["1", 2]]
        self.testdict = dict(a=1, b=2.5j)
        self.testClassInt = ClassInt()

    @classmethod
    def _complex_handler(clsself, Obj):
        if hasattr(Obj, '__dict__'):
            return Obj.__dict__
        else:
            raise TypeError('Test Type-Error')

    @classmethod
    def ToJSON(clsself, obj, ind=0):
        return json.dumps(obj.__dict__, default=clsself._complex_handler, indent=ind)


class ClassInt():
    def __init__(self):
        self.int = 1
