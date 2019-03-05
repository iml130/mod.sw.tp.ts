#    Copyright 2018 Fraunhofer IML
#
#    Licensed under the Apache License, Version 2.0 (the "License");
#    you may not use this file except in compliance with the License.
#    You may obtain a copy of the License at
#
#        http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS,
#    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#    See the License for the specific language governing permissions and
#    limitations under the License.

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
        entity.setObject(ComplexExample(), {}, False)
        ComplexExample().ToJSON(entity)
        # No Error thrown

    def test_EntityAttributeBool(self):
        ea = EA(True, False)
        self.assertTrue(not hasattr(ea, 'metadata'))
        self.assertEqual(ea.value, True)
        self.assertEqual(ea.type, "boolean")

        ea = EA(False, False)
        self.assertTrue(not hasattr(ea, 'metadata'))
        self.assertEqual(ea.value, False)
        self.assertEqual(ea.type, "boolean")

    def test_EntityAttributeInt(self):
        ea = EA(1, False)
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="int")))
        self.assertEqual(ea.value, 1)
        self.assertEqual(ea.type, "number")

    def test_EntityAttributeFloat(self):
        ea = EA(2.132, False)
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="float")))
        self.assertEqual(ea.value, 2.132)
        self.assertEqual(ea.type, "number")

    def test_EntityAttributeLong(self):
        ea = EA(42L, False)
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="long")))
        self.assertEqual(ea.value, 42L)
        self.assertEqual(ea.type, "number")

    def test_EntityAttributeComplex(self):
        ea = EA(complex(3, 1), False)
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="complex")))
        self.assertEqual(ea.value[0].value, 3)
        self.assertEqual(ea.value[1].value, 1)
        self.assertEqual(ea.type, "array")

        ea = EA(2.34j, False)
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="complex")))
        self.assertEqual(ea.value[0].value, 0)
        self.assertEqual(ea.value[1].value, 2.34)
        self.assertEqual(ea.type, "array")

    def test_EntityAttributeString(self):
        ea = EA("Hello world!", False)
        self.assertTrue(not hasattr(ea, 'metadata'))
        self.assertEqual(ea.value, "Hello world!")
        self.assertEqual(ea.type, "string")

    def test_EntityAttributeUnicode(self):
        ea = EA(u'Unicode', False)
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="unicode")))
        self.assertEqual(ea.value, u'Unicode')
        self.assertEqual(ea.type, "string")

    def test_EntityAttributeTuple(self):
        ea = EA((1, 2), False)
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="tuple")))
        self.assertTrue(isinstance(ea.value, list))
        self.assertEqual(ea.value[0].value, 1)
        self.assertEqual(ea.value[1].value, 2)
        self.assertEqual(ea.type, "array")

    def test_EntityAttributeList(self):
        ea = EA([1, 2], False)
        self.assertTrue(not hasattr(ea, 'metadata'))
        self.assertTrue(isinstance(ea.value, list))
        self.assertEqual(ea.value[0].value, 1)
        self.assertEqual(ea.value[1].value, 2)
        self.assertEqual(ea.type, "array")

    def test_EntityAttributeDict(self):
        ea = EA(dict(a=1, b=2), False)
        self.assertTrue(not hasattr(ea, 'metadata'))
        self.assertTrue(isinstance(ea.value, dict))
        self.assertEqual(ea.value.get('a').value, 1)
        self.assertEqual(ea.value.get('b').value, 2)
        self.assertEqual(ea.type, "object")

    def test_EntityAttributeForeignClass(self):
        ea = EA(ClassInt(), False)
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="class")))
        self.assertEqual(ea.type, "ClassInt")
        self.assertTrue(ea.value != None)

    def test_EntityAttributeComplex_ignoreMetaData_True(self):
        ea = EA(complex(3, 1), True)
        self.assertTrue(not hasattr(ea, 'metadata'))
        self.assertEqual(ea.value[0].value, 3)
        self.assertEqual(ea.value[1].value, 1)
        self.assertEqual(ea.type, "array")

    def test_EntityAttributeFloat32List_concreteDataType(self):
        ea = EA(ClassInt(), True, concreteDataType=dict(int="uint32_t"))
        self.assertTrue(hasattr(ea, 'metadata'))
        self.assertEqual(ea.metadata, dict(
            dataType=dict(type="dataType", value=dict(int='uint32_t'))))
        self.assertEqual(ea.value['int'].value, 1)
        self.assertEqual(ea.type, "ClassInt")

    def test_EntityAttributeForeignRosClass(self):
        ea = EA(RosClassWithSlotsInt(), False)
        self.assertEqual(ea.metadata, dict(
            python=dict(type="dataType", value="class")))
        self.assertEqual(ea.type, "RosClass.Integer") # Slashes are not allowed!
        self.assertTrue(ea.value != None)


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
        self.testClassInt = [ClassInt()]*10 # Test id Array is supported
        self.testClassInt = ClassSlotsInt()
        self.testClassInt = [ClassSlotsInt()]*10 # Test id Array is supported

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


class ClassSlotsInt(object):
    __slots__ = ['val1']
    def __init__(self):
        self.val1 = 1

class RosClassWithSlotsInt(object):
    __slots__ = ['val1', '_type']
    def __init__(self):
        self.val1 = 1
        self._type = "RosClass/Integer"  # Example-Type

