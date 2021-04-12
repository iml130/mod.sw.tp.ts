""" Contains FiwareEntity class """

import uuid


from tasksupervisor.helpers.utc import get_utc_time

class FiwareEntity():
    __initialized = False
    """ Base representation of an Entity for FIWAREs Orion Context Broker
        id - represents the unique id of an entity
        type - represents the type of an entity

        caution - An entity is unique through its id+type+servicepath
     """

    def __init__(self, id=None):
        self.type = self.__class__.__name__
        if id is None:
            self.id = self.type + str(uuid.uuid4())
        else:
            self.id = str(id)
        self.__initialized = True

    def get_entity(self):
        print("Create Entity: id: " + self.get_id() + ", type: " + self.get_type())

        return {"id": self.get_id(), "type": self.get_type()}

    def get_type(self):
        """ Returns the type of an entity """
        return self.type

    def get_id(self):
        """ Returns the unique ID of an entity """
        return self.id


    def update_time(self):
        self.updateTime = get_utc_time()

    def __setattr__(self, name, value):
        if self.__initialized and not name == "updateTime" and not name.startswith("_"):
            self.update_time()
        super().__setattr__(name, value)

    def obj2JsonArray(self):
        temp_array = []
        temp_array.append(self.get_entity())

        return temp_array
