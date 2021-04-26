""" Contains SensorAgent and SensorData API class """

import uuid

class SensorData(object):
    def __init__(self, **entries):
        self.readings = []

        self.__dict__.update(entries)  # Insert values from given dict

class SensorAgent():
    """ Representation of a real world sensor """
    def __init__(self, _id=None):
        self.id = uuid.uuid4()
        self.type = "SensorAgent"
        self.measurement_type = ""
        self.modified_time = ""  # ISO8601
        self.readings = []  # List of SensorData
        self.san_id = ""
        self.sensor_id = ""
        self.sensor_manufacturer = ""
        self.sensor_type = ""
        self.units = ""

    def find_sensor_by_id(self, trigger_name):
        trigger_name = trigger_name.split(".")[0]
        for sdata in self.sensorData:
            if sdata.sensor_id == trigger_name:
                return sdata
        return None
