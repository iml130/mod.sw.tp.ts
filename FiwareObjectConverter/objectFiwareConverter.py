""" This Module converts Python-Objects into the Fiware-JSON-Format.
    For more Information how to use this class, see the Readme.md
    You can find the needed Files to convert from an Object into JSON
    in the folder JsonToObject and vice versa
"""
__author__ = "Dominik Lux"
__credits__ = ["Peter Detzner"]
__maintainer__ = "Dominik Lux"
__version__ = "0.0.1a"
__status__ = "Developement"

from JsonToObject.reverseEntity import ReverseEntity
from ObjectToJson.entity import Entity
import json


class ObjectFiwareConverter(object):
    """ This class should be primarily used to convert a Object <-> JSON-string.
        The classes in subdirectories are either used to convert them into JSON
        or into a Python-specific-Object. 
    """

    @classmethod
    def obj2Fiware(clsself, _object, ind=0, dataTypeDict={}, ignorePythonMetaData=False, showIdValue = True): 
        en = Entity()
        en.setObject(_object, dataTypeDict, ignorePythonMetaData, showIdValue= showIdValue)
 
        return clsself._json(en, ind)

    @classmethod
    def fiware2Obj(clsself, _fiware_str, _objectStructure={}, useMetadata=True, ignoreWrongDataType=False, setAttr=False):
        if(type(_fiware_str) is dict):
            _fiware_str = json.dumps(_fiware_str)
        jsonObj = clsself._obj(_fiware_str)
        re = ReverseEntity(**jsonObj)
        return re.setObject(_objectStructure, useMetadata, ignoreWrongDataType, setAttr) 

    @classmethod
    def _complex_handler(clsself, Obj):
        if hasattr(Obj, '__dict__'):
            return Obj.__dict__
        else:
            raise TypeError('Object of type %s with value of %s is not JSON serializable' % (
                type(Obj), repr(Obj)))

    @classmethod
    def _json(clsself, obj, ind=0):
        return json.dumps(obj.__dict__, default=clsself._complex_handler, indent=ind)

    @classmethod
    def _obj(clsself, json_str):
        return json.loads(json_str)
