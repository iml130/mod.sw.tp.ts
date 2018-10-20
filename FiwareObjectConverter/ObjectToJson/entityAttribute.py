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

    def __init__(self, _object):
        self.value = _object
        self.type = ""
        self.metadata = {}
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
            self.metadata = dict(python=dict(type="dataType", value="int"))
        elif objectType is float:
            self.type = "number"
            self.value = float(_object)
            self.metadata = dict(python=dict(type="dataType", value="float"))
        elif objectType is long:
            self.type = "number"
            self.value = long(_object)
            self.metadata = dict(python=dict(type="dataType", value="long"))
        elif objectType is complex:
            self.type = "array"
            t = complex(_object)
            self.value = [EntityAttribute(t.real), EntityAttribute(t.imag)]
            self.metadata = dict(python=dict(type="dataType", value="complex"))
        elif objectType is str:
            self.type = "string"
            self.value = str(_object)
        elif objectType is unicode:
            self.type = "string"
            self.value = unicode(_object)
            self.metadata = dict(python=dict(type="dataType", value="unicode"))
        elif objectType is tuple:
            self.type = "array"
            self.value = []
            self.metadata = dict(python=dict(type="dataType", value="tuple"))
            for item in _object:
                self.value.append(EntityAttribute(item))
        elif objectType is list:
            self.type = "array"
            self.value = []
            for item in _object:
                self.value.append(EntityAttribute(item))
        elif objectType is dict:
            self.type = "object"
            tempDict = {}
            for key, value in _object.iteritems():
                tempDict[key] = EntityAttribute(value)
            self.value = tempDict
        else:
            # Case it is a Class
            self.type = _object.__class__.__name__
            self.metadata = dict(python=dict(type="dataType", value="class"))
            tempDict = {}
            for key, value in _object.__dict__.iteritems():
                tempDict[key] = EntityAttribute(value)
            self.value = tempDict
