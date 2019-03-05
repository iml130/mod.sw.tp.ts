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
from entity import Entity


class Test_JsonConverter(unittest.TestCase):

    def test_EntityInitializeIsNotEmpty(self):
        en = Entity()
        self.assertEqual(en.type, "Entity")
        self.assertEqual(en.id[0:6], "Entity")

    def test_Entitiy_setObejct_Primitve(self):
        en = Entity()
        try:
            en.setObject(1, {}, False)
        except ValueError:
            self.assertTrue(True)

    def test_Entitiy_setObejct_Non_Primitve(self):
        en = Entity()
        en.setObject(TestClass(), {}, False)
        self.assertEqual(en.id[0:9], "TestClass")
        self.assertEqual(en.type, "TestClass")
        self.assertEqual(en.__dict__['value'].value, 1)

    def test_Entitiy_setObejct_Non_Primitve_WITH_given_type_id(self):
        en = Entity()
        en.setObject(TypeIDTestClass(), {}, False)
        self.assertEqual(en.id[0:9], "MyId")
        self.assertEqual(en.type, "This should NOT be overwritten")
        self.assertEqual(en.__dict__['value'].value, 1)


class TestClass(object):
    def __init__(self):
        self.value = 1


class TypeIDTestClass(object):
    def __init__(self):
        self.value = 1
        self.type = "This should NOT be overwritten"  # Needed behaviour, so that the user can decide the type and id
        self.id = "MyId"
