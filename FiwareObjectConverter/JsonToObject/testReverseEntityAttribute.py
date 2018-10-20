__author__ = "Dominik Lux"
__credits__ = ["Peter Detzner"]
__maintainer__ = "Dominik Lux"
__version__ = "0.0.1a"
__status__ = "Developement"

import unittest
from reverseEntityAttribute import ReverseEntityAttribute


class TestEntityAttribute(unittest.TestCase):

    def test_ReverseEntityAttributeBool(self):
        d = dict(type="boolean", value=True, metadata={})
        rea = ReverseEntityAttribute(d)
        self.assertEqual(True, rea.getValue())
        self.assertEqual(type(rea.getValue()), bool)

    def test_ReverseEntityAttributeInt(self):
        d = dict(type="number", value=1, metadata=dict(
            python=dict(type="dataType", value="int")))
        rea = ReverseEntityAttribute(d)
        self.assertEqual(1, rea.getValue())
        self.assertEqual(type(rea.getValue()), int)

    def test_ReverseEntityAttributeFloat(self):
        d = dict(type="number", value=2.132, metadata=dict(
            python=dict(type="dataType", value="float")))
        rea = ReverseEntityAttribute(d)
        self.assertEqual(2.132, rea.getValue())
        self.assertEqual(type(rea.getValue()), float)

    def test_ReverseEntityAttributeLong(self):
        d = dict(type="number", value=42L, metadata=dict(
            python=dict(type="dataType", value="long")))
        rea = ReverseEntityAttribute(d)
        self.assertEqual(42L, rea.getValue())
        self.assertEqual(type(rea.getValue()), long)

    def test_ReverseEntityAttributeComplex(self):
        d = dict(type="array",
                 value=[dict(type="number",   value=0,   metadata=dict(python=dict(type="dataType", value="int"))),
                        dict(type="number", value=2.34, metadata=dict(python=dict(type="dataType", value="int")))],
                 metadata=dict(python=dict(type="dataType", value="complex")))
        rea = ReverseEntityAttribute(d)
        self.assertEqual(2.34j, rea.getValue())
        self.assertEqual(type(rea.getValue()), complex)

    def test_ReverseEntityAttributeString(self):
        d = dict(type="string", value="Hello world!", metadata={})
        rea = ReverseEntityAttribute(d)
        self.assertEqual("Hello world!", rea.getValue())
        self.assertEqual(type(rea.getValue()), str)

    def test_ReverseEntityAttributeUnicode(self):
        d = dict(type="string", value=u'Unicode',
                 metadata=dict(python=dict(type="dataType", value="unicode")))
        rea = ReverseEntityAttribute(d)
        self.assertEqual(u'Unicode', rea.getValue())
        self.assertEqual(type(rea.getValue()), unicode)

    def test_ReverseEntityAttributeTuple(self):
        d = dict(type="array", value=[dict(type="number", value=1, metadata=dict(python=dict(type="dataType", value="int"))), dict(
            type="number", value=2, metadata=dict(python=dict(type="dataType", value="int")))], metadata=dict(python=dict(type="dataType", value="tuple")))
        rea = ReverseEntityAttribute(d)
        self.assertEqual(tuple((1, 2)), rea.getValue())
        self.assertEqual(type(rea.getValue()), tuple)

    def test_ReverseEntityAttributeList(self):
        d = dict(
            type="array",
            value=[dict(type="number", value=1, metadata=dict(python=dict(type="dataType", value="int"))),
                   dict(type="number", value=2, metadata=dict(python=dict(type="dataType", value="int")))],
            metadata={})
        rea = ReverseEntityAttribute(d)
        self.assertEqual(list([1, 2]), rea.getValue())
        self.assertEqual(type(rea.getValue()), list)

    def test_ReverseEntityAttributeDict(self):
        d = dict(type="object", value=dict(
            a=dict(type="number", value=1, metadata=dict(
                python=dict(type="dataType", value="int"))),
            b=dict(type="number", value=2, metadata=dict(python=dict(type="dataType", value="int")))),
            metadata={})

        rea = ReverseEntityAttribute(d)
        self.assertEqual(dict(a=1, b=2), rea.getValue())
        self.assertEqual(type(rea.getValue()), dict)

    def test_ReverseEntityAttributeForeignClass(self):
        d = dict(type="ClassInt",
                 value=dict(int=dict(type="number", value=1, metadata=dict(
                     python=dict(type="dataType", value="int")))),
                 metadata=dict(python="class"))

        rea = ReverseEntityAttribute(d)
        self.assertEqual(dict(int=1), rea.getValue())
        self.assertEqual(type(rea.getValue()), dict)
