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

### Error Messages
TYPE_VALUE_METADATA_NOT_DEFINED_MESSAGE = "One of the following is not defined in json: {type|value}"
VALUE_EMPTY_MESSAGE = "The Value entered cannot be empty!"

### Types which can be retrieved from the JSON:
NUMERICAL_TYPES = ["number", "integer", "int", "float", "double", "long", ]
TEXT_TYPES = ["string",  "text"]
BOOLEAN_TYPES = ["bool",  "boolean"]
ARRAYLIKE_TYPES = ["array", "list", "tuple", "vector"]
OBJECTLIKE_TYPES = ["object", "obj"]


class ReverseEntityAttribute(object):
    """ Here the actual Conversion happens. 
        By initiliazing the class, the _dict is translated into the 
        primitive datatypes. With the variable useMetadata the metadata can be ignored
        It defaults then from:
        Complex, Tuple -> List
        Unicode -> String
    """

    def __init__(self, _dict, useMetadata=True):
        """ By initializing we set the value in self.value
        """
        self.value = None

        if _dict is None:
            raise ValueError(VALUE_EMPTY_MESSAGE)

        if 'type' not in _dict or 'value' not in _dict:
            # Check if a correct struct exists.
            raise ValueError(TYPE_VALUE_METADATA_NOT_DEFINED_MESSAGE)

        if not 'metadata' in _dict:
            useMetadata=False


        # Back Conversion:
        if _dict['type'] == '' :
            self.value = _dict['value']

        elif _dict['type'].lower() in BOOLEAN_TYPES:
            self._setValue(bool, _dict['value'])

        elif  _dict['type'].lower() in NUMERICAL_TYPES:
            # Case something numerical
            self._setValue(float, _dict['value'])
            if self.value % 1 == 0.0: 
                # Number is Integer Like, convert to int or long
                self._setValueWithMetadata([int, long], useMetadata, _dict, self.value)

        elif _dict['type'].lower() in TEXT_TYPES:
            # Case String or Unicode
            self._setValueWithMetadata([unicode, str], useMetadata, _dict, _dict['value'])

        elif _dict['type'].lower() in ARRAYLIKE_TYPES:
            # Case Complex, Tuple or List
            # First: reverse every element to Obj
            tempList = _dict['value']
            tempValue = list()
            for value in tempList:
                re = ReverseEntityAttribute(value, useMetadata)
                tempValue.append(re.getValue())

            # Second: decide if Complex, Tuple or List
            self._setValueWithMetadata([complex, tuple, list], useMetadata, _dict, tempValue)

        elif _dict['type'].lower() in OBJECTLIKE_TYPES:
            # arbitary JSON object with key, value
            tempDict = _dict['value']
            self.value = {}
            for key, value in tempDict.iteritems():
                rea = ReverseEntityAttribute(value, useMetadata)
                self.value[key] = rea.getValue()

        else:
            # Maybe a class with key, value or another JSON object, check if you can iterate!
            if (not hasattr(_dict['value'], 'iteritems')):
                raise ValueError("Unknown Object-Type: " + _dict['type'] + ". And it is not possible to iterate over this Object-Type!")

            tempDict = {}
            for key, value in _dict['value'].iteritems():
                rea = ReverseEntityAttribute(value, useMetadata)
                tempDict[key] = rea.getValue()
            self.value = tempDict


    def getValue(self):
        return self.value


    def _setValue(self, targetType, value):
        """ This function sets self.value  . 
            Complex needs to be called differently
            and we need to check if the input of bool is a string
        """
        if targetType == bool and type(value) == str:
            self.value = value.lower in ["false", "f", "0"]
        elif targetType != complex:
            self.value = targetType(value)
        else: 
            self.value = targetType(*value)


    def _setValueWithMetadata(self, targetTypes, useMetadata, readict, value):
        """ This function sets the Value, dependent on the given metadata.
            If no metadata is given or it does not contain the correct format,
            we default to the last element of targetTypes
        """
        if useMetadata and 'python' in readict['metadata']:
            metadata = readict['metadata']

            # we try to find a valid dataType
            for tt in targetTypes:
                if metadata['python'] == dict(type="dataType", value=tt.__name__):
                    self._setValue(tt, value)
                    return
            
            # Case: we did not set self.value, we default to the last element
            self._setValue(targetTypes[-1], value)
        else:
            # Case: no metadata, we also default to the last element
            self._setValue(targetTypes[-1], value)
