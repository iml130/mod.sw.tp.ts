__author__ = "Dominik Lux"
__credits__ = ["Peter Detzner"]
__maintainer__ = "Dominik Lux"
__version__ = "0.0.1a"
__status__ = "Developement"

TYPE_VALUE_METADATA_NOT_DEFINED_MESSAGE = "One of the following is not defined in json: {type|value|metadata}"
VALUE_EMPTY_MESSAGE = "The Value entered is empty!"


class ReverseEntityAttribute(object):
    """ Here the actual Conversion happens. 
        By initiliazing the class, the _dict is translated into the 
        primitive datatypes. With the variable useMetadata the metadata can be ignored
        It defaults then from:
        Complex, Tuple -> List
        Unicode -> String

    """

    def __init__(self, _dict, useMetadata=True):
        """ throw Error!!
        """
        self.value = None

        if _dict is None:
            raise ValueError(VALUE_EMPTY_MESSAGE)

        if 'type' not in _dict or 'value' not in _dict:
            # Check if a viable struct exists.
            raise ValueError(TYPE_VALUE_METADATA_NOT_DEFINED_MESSAGE)

        if _dict['type'] == '' or _dict['type'] == 'boolean' or _dict['type'] == 'number' or _dict['type']=="Integer":
            # We don't care about primitive types just set them
            self.value = _dict['value']

        elif _dict['type'] == 'string':
            # Case String or Unicode
            if 'python' in _dict['metadata'] and useMetadata:
                metadata = _dict['metadata']
                if metadata['python'] == dict(type="dataType", value="unicode"):
                    self.value = unicode(_dict['value'])
                    return
            # defaulting to str
            self.value = str(_dict['value'])

        elif _dict['type'] == 'array':
            # Case Complex, Tuple or List
            # First: reverse every element to Obj
            tempList = _dict['value']
            tempValue = list()
            for value in tempList:
                re = ReverseEntityAttribute(value, useMetadata)
                tempValue.append(re.getValue())

            # Second: decide if Complex, Tuple or List
            if 'python' in _dict['metadata'] and useMetadata:
                metadata = _dict['metadata']
                if metadata['python'] == dict(type="dataType", value="complex"):
                    self.value = complex(*tempValue)
                    return
                elif metadata['python'] == dict(type="dataType", value="tuple"):
                    self.value = tuple(tempValue)
                    return
            # defaulting to list
            self.value = list(tempValue)

        elif _dict['type'] == 'object':
            # arbitary JSON object with key, value
            tempDict = _dict['value']
            self.value = {}
            for key, value in tempDict.iteritems():
                re = ReverseEntityAttribute(value, useMetadata)
                self.value[key] = re.getValue()

        else:
            # Maybe a class with key, value or another JSON object
            tempDict = {}
            for key, value in _dict['value'].iteritems():
                rea = ReverseEntityAttribute(value, useMetadata)
                tempDict[key] = rea.getValue()
            self.value = tempDict

    def getValue(self):
        return self.value
