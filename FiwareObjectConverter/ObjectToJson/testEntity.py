__author__ = "Dominik Lux"
__credits__ = ["Peter Detzner"]
__maintainer__ = "Dominik Lux"
__version__ = "0.0.1a"
__status__ = "Developement"

import unittest
from entity import Entity


class Test_JsonConverter(unittest.TestCase):

    def test_EntityInitializeIsNotEmpty(self):
        en = Entity()
        self.assertEqual(en.type, "Entity")
        self.assertEqual(en.id[0:6], "Entity")

    def test_EntitiysetObejct_Primitve(self):
        en = Entity()
        try:
            en.setObject(1)
        except ValueError:
            self.assertTrue(True)

    def test_EntitiysetObejct_Non_Primitve(self):
        en = Entity()
        en.setObject(TestClass())
        self.assertEqual(en.id[0:9], "TestClass")
        self.assertEqual(en.type, "TestClass")
        self.assertEqual(en.__dict__['value'].value, 1)


class TestClass(object):
    def __init__(self):
        self.value = 1
        self.type = "This should be overwritten"
