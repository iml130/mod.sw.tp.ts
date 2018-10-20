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


class TestJson(object):
    def __init__(self):
        self.variableName = 0  # Set type int!
        self.notDefinedVarByJSON = 42
