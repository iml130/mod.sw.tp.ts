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

from reverseEntityAttribute import ReverseEntityAttribute

MISMATCH_MESSAGE = "The Class-Type does not match with the JSON-type!"


class ReverseEntity(object):
    """ A simple class which reconverts from JSON into a __dict__.
        The Function setObject decides if type check (ignoreWrongDataType)
        is used and adds the (if the key from JSON is also in obj) value to the obj.
        'setAttr' is here explicitly used, if set to true.
    """

    def __init__(self, type, id, *args, **payload):
        self.type = type
        self.id = id
        self.payload = payload

    def setObject(self, obj, useMetadata=True, ignoreWrongDataType=False, setAttr=False):
        # Explicitly set id and type, always!
        setattr(obj, 'id', self.id)
        setattr(obj, 'type', self.type)
        
        for key, value in self.payload.iteritems():
            rea = ReverseEntityAttribute(value, useMetadata)
            if (setAttr):
                # Just use setAttr
                setattr(obj, key, rea.getValue())
            elif key in obj.__dict__:
                if (ignoreWrongDataType):
                    # Ignoring expected Data-Type
                    obj.__dict__[key] = rea.getValue()
                else:
                    val = rea.getValue()
                    if type(obj.__dict__[key]) is not type(val):
                        raise TypeError(MISMATCH_MESSAGE)
                    else:
                        obj.__dict__[key] = val
