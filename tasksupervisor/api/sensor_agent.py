# using enum34
from enum import IntEnum

from tasksupervisor.entities.entity import FiwareEntity
from fiwareobjectconverter.object_fiware_converter import ObjectFiwareConverter


class SensorData(object):
    def __init__(self, **entries):
        self.readings = []

        self.__dict__.update(entries)  # Insert values from given dict


class SensorAgent():
    def __init__(self, _id=None):
        self.type = "SensorAgent"
        self.measurementType = ""
        self.modifiedTime = ""  # ISO8601
        self.readings = []  # List of SensorData
        self.sanID = ""
        self.sensorID = ""
        self.sensorManufacturer = ""
        self.sensorType = ""
        self.units = ""

    def findSensorById(self, _trigger_name):
        _trigger_name = _trigger_name.split(".")[0]
        for sdata in self.sensorData:
            if(sdata.sensorId == _trigger_name):
                return sdata
        return None
