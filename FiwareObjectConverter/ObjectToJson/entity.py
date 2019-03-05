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

__author__ = "Peter Detzner"
__credits__ = ["Peter Detzner"]
__maintainer__ = "Dominik Lux"
__version__ = "0.0.1a"
__status__ = "Developement"

import uuid
from entityAttribute import EntityAttribute

ERROR_MESSAGE_ATTTRIBUTE = 'Error setting Object in \'setObject\' : '


class Entity(object):
    """ This is the Entity which will be later serialized with json. 
        Here the __dict__ is set with setObject. Also th uuid is here generated and
        all types are converted into correct structure with EntityAttribute.
        The Keys "type" "id" and "_*" are ignored and not added into the Entity
    """

    def __init__(self):
        self.type = self.__class__.__name__
        self.id = self.type + str(uuid.uuid4())

    def setObject(self, _object, dataTypeDict, ignorePythonMetaData, showIdValue = True ):
        # Clear own dictionary
        self.__dict__.clear()
        try:
            # Setting EntityType and EntitiyID
            if (showIdValue):
                self.type = _object.__class__.__name__
                self.id = self.type + str(uuid.uuid4())


            # Set Key/Value in own Dictionary
            if (isinstance(_object, dict)):
                iterL = _object.keys()
            elif(hasattr(_object, '__slots__')):
                iterL = getattr(_object, '__slots__')
            else:
                iterL = _object.__dict__

            for key in iterL:
                # Explicitly set id and type if it exists
                if (key == "id" and showIdValue):
                    if (isinstance(_object, dict)):
                        self.id = _object[key]
                    else:
                        self.id = getattr(_object, key) 
                elif (key == "type" and showIdValue):
                    if (isinstance(_object, dict)):
                        self.type = _object[key]
                    else:
                        self.type = getattr(_object, key) 

                if (isinstance(_object, dict)):
                    value = _object[key]
                else:
                    value = getattr(_object, key)
                if (key == "type" or key == "id" or key.startswith('_', 0, 1)):
                    # Object contains invalid key-name, ignore!
                    pass
                else:
                    self.__dict__[key] = EntityAttribute(value, ignorePythonMetaData, dataTypeDict.get(key)) 
        except AttributeError as ex:
            raise ValueError(ERROR_MESSAGE_ATTTRIBUTE, ex)

    def __repr__(self):
        return "Id: " + str(self.id) + ", Type: " + str(self.type)
