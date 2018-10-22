__author__ = "Dominik Lux"
__credits__ = ["Peter Detzner"]
__maintainer__ = "Dominik Lux"
__version__ = "0.0.1a"
__status__ = "Developement"

from reverseEntityAttribute import ReverseEntityAttribute

MISMATCH_MESSAGE = "The Class-Type does not match with the JSON-type!"


class ReverseEntity(object):
    """ A simple class which reconverts from JSON into a __dict__.
        the Function setObject decides, whether to type check (ignoreWrongDataType)
        and adds the (if the key from JSON is also in obj) value to the obj
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
                setattr(obj, key, rea.getValue())
            elif key in obj.__dict__:
                if (ignoreWrongDataType):
                    # Not bidirectional
                    obj.__dict__[key] = rea.getValue()
                else:
                    val = rea.getValue()
                    if type(obj.__dict__[key]) is not type(val):
                        raise TypeError(MISMATCH_MESSAGE)
                    else:
                        obj.__dict__[key] = val
