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

    def setObject(self, _object):
        # Clear own dictionary
        self.__dict__.clear()
        try:
            # Setting EntityType and EntitiyID
            self.type = _object.__class__.__name__
            self.id = self.type + str(uuid.uuid4())

            # Set Key/Value in own Dictionary
            for key, value in _object.__dict__.iteritems():
                if (key == "type" or key == "id" or key.startswith('_', 0, 1)):
                    # Object contains invalid key-name, ignore!
                    pass
                else:
                    self.__dict__[key] = EntityAttribute(value)
        except AttributeError as ex:
            raise ValueError(ERROR_MESSAGE_ATTTRIBUTE, ex)

    def __repr__(self):
        return "Id: " + str(self.id) + ", Type: " + str(self.type)
