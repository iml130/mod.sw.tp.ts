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

from reverseEntity import ReverseEntity


class TestReverseEntity(unittest.TestCase):

    def test_ReverseEntityInitializeIsNotEmpty(self):
        d = dict(type="MyJSONType", id="MyJSONTypeID", variableName=dict(
            type="number", value=1, metadata=dict(python=dict(type="dataType", value="int"))))

        en = ReverseEntity(**d)
        self.assertEqual(en.type, "MyJSONType")
        self.assertEqual(en.id, "MyJSONTypeID")
        self.assertEqual(en.payload, dict(variableName=dict(
            type="number", value=1, metadata=dict(python=dict(type="dataType", value="int")))))

    def test_ReverseEntityInitializeIsEmptyPayload(self):
        d = dict(type="MyJSONType", id="MyJSONTypeID")

        en = ReverseEntity(**d)
        self.assertEqual(en.type, "MyJSONType")
        self.assertEqual(en.id, "MyJSONTypeID")
        self.assertEqual(en.payload, {})

    def test_ReverseEntitiysetObejctInstantiate(self):
        d = dict(type="MyJSONType", id="MyJSONTypeID", variableName=dict(
            type="number", value=1, metadata=dict(python=dict(type="dataType", value="int"))))
        en = ReverseEntity(**d)
        self.assertEqual(en.type, "MyJSONType")
        self.assertEqual(en.id, "MyJSONTypeID")
        self.assertEqual(en.payload, dict(variableName=dict(
            type="number", value=1, metadata=dict(python=dict(type="dataType", value="int")))))

        tj = TestJson()
        en.setObject(tj)

        self.assertEqual(tj.variableName, 1)
        self.assertEqual(tj.notDefinedVarByJSON, 42)

    def test_ReverseEntitiysetObejctInstantiate_IgnoreWrongDataTypes(self):
        d = dict(type="MyJSONType", id="MyJSONTypeID", variableName=dict(
            type="number", value=1.5, metadata=dict(python=dict(type="dataType", value="float"))))
        en = ReverseEntity(**d)
        self.assertEqual(en.type, "MyJSONType")
        self.assertEqual(en.id, "MyJSONTypeID")
        self.assertEqual(en.payload, dict(variableName=dict(
            type="number", value=1.5, metadata=dict(python=dict(type="dataType", value="float")))))

        tj = TestJson()
        en.setObject(tj, ignoreWrongDataType=True)

        self.assertEqual(tj.variableName, 1.5)
        self.assertEqual(type(tj.variableName), float)
        self.assertEqual(tj.notDefinedVarByJSON, 42)

    def test_ReverseEntitiysetObejctInstantiate_setAttr_True(self):
        d = dict(type="MyJSONType", id="MyJSONTypeID", variableName=dict(
            type="number", value=1.5, metadata=dict(python=dict(type="dataType", value="float"))))
        en = ReverseEntity(**d)
        self.assertEqual(en.type, "MyJSONType")
        self.assertEqual(en.id, "MyJSONTypeID")
        self.assertEqual(en.payload, dict(variableName=dict(
            type="number", value=1.5, metadata=dict(python=dict(type="dataType", value="float")))))

        tj = TestJson()
        en.setObject(tj, setAttr=True)

        self.assertEqual(tj.variableName, 1.5)
        self.assertEqual(type(tj.variableName), float)
        self.assertEqual(tj.notDefinedVarByJSON, 42)

    def test_ReverseEntitiysetObejctInstantiate_setAttr_False(self):
        d = dict(type="MyJSONType", id="MyJSONTypeID", variableName=dict(
            type="number", value=1.5, metadata=dict(python=dict(type="dataType", value="float"))))
        en = ReverseEntity(**d)
        self.assertEqual(en.type, "MyJSONType")
        self.assertEqual(en.id, "MyJSONTypeID")
        self.assertEqual(en.payload, dict(variableName=dict(
            type="number", value=1.5, metadata=dict(python=dict(type="dataType", value="float")))))

        tj = TestJson()
        try: 
            en.setObject(tj, setAttr=False)
            self.fail()
        except TypeError:
            pass
            # Success!!


class TestJson(object):
    def __init__(self):
        self.variableName = 0  # Set type int!
        self.notDefinedVarByJSON = 42
