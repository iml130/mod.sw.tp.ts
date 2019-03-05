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


class EntityAttribute():
    """ Here the actual Conversion to the correct JSON-Format happens 
    (no string is generated here). By initializing this class the given Object is 
    translated into the format. This is straight-forward if-then-else-magic.
    Additional information are given for some types, for a bidirectional Conversion.

    """

    def __init__(self, _object, ipmd, concreteDataType=None):  
        self.value = _object
        self.type = ""
        self.metadata = dict()
        objectType = type(_object)


        # Simply if-then-else to the Json fromat
        if(objectType is type(None)):
            pass
        elif objectType is bool:
            self.type = "boolean"
            self.value = bool(_object)
        elif objectType is int:
            self.type = "number"
            self.value = int(_object)
            self.setPythonMetaData(ipmd, "int")
        elif objectType is float:
            self.type = "number"
            self.value = float(_object)
            self.setPythonMetaData(ipmd, "float")
        elif objectType is long:
            self.type = "number"
            self.value = long(_object)
            self.setPythonMetaData(ipmd, "long")
        elif objectType is complex:
            self.type = "array"
            t = complex(_object)
            self.value = [EntityAttribute(t.real, ipmd), EntityAttribute(t.imag, ipmd)]
            self.setPythonMetaData(ipmd, "complex")
        elif objectType is str:
            self.type = "string"
            self.value = str(_object)
        elif objectType is unicode:
            self.type = "string"
            self.value = unicode(_object)
            self.setPythonMetaData(ipmd, "unicode")
        elif objectType is tuple:
            self.type = "array"
            self.value = []
            self.setPythonMetaData(ipmd, "tuple")
            for item in _object:
                self.value.append(EntityAttribute(item, ipmd))
        elif objectType is list:
            self.type = "array"
            self.value = []
            for item in _object:
                self.value.append(EntityAttribute(item, ipmd))
        elif objectType is dict:
            self.type = "object"
            tempDict = {}
            for key, value in _object.iteritems():
                tempDict[key] = EntityAttribute(value,ipmd )
            self.value = tempDict
        else:
            # Case it is a Class
            # check explicitly if it has the needed attrs
            if (hasattr(_object, '__slots__')):
                iterL = getattr(_object, '__slots__')
            elif(hasattr(_object, '__dict__')):
                iterL = _object.__dict__
            else:
                raise ValueError("Cannot get attrs from {}".format(str(_object)))

            if hasattr(_object, '_type'):   # ROS-Specific Type-Declaration
                self.type = _object._type.replace("/", ".") # Needs to be replaced Fiware does not allow a '/'
            else:
                self.type = _object.__class__.__name__
            self.setPythonMetaData(ipmd, "class")
            tempDict = {}
            for key in iterL:
                tempDict[key] = EntityAttribute(getattr(_object, key), ipmd)
            self.value = tempDict


        if concreteDataType is not None:
            self.metadata["dataType"] = dict(type="dataType", value=concreteDataType)
            pass

        # Remove metadata-Attribute if it is empty (minimizing the JSON)
        if self.metadata == {} :
            delattr(self, "metadata")

    def setPythonMetaData(self, ignorePythonMetaData, val):
        if not ignorePythonMetaData:
            self.metadata["python"] = dict(type="dataType", value=val)
    