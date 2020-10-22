# using enum34
from enum import IntEnum

from tasksupervisor.entities.entity import FiwareEntity
from fiwareobjectconverter.object_fiware_converter import ObjectFiwareConverter


class SensorData(object):
    def __init__(self, **entries):
        self.readings = []

        self.__dict__.update(entries)  # Insert values from given dict


class SensorAgent(FiwareEntity):
    def __init__(self, _id=None):
        FiwareEntity.__init__(self, id=_id)
        self.type = "SensorAgent"
        self.measurementType = ""
        self.modifiedTime = ""  # ISO8601
        self.readings = []  # List of SensorData
        self.sanID = ""
        self.sensorID = ""
        self.sensorManufacturer = ""
        self.sensorType = ""
        self.units = ""

    @classmethod
    def CreateObjectFromJson(cls, _my_json):
        sa = SensorAgent()
        try:
            ObjectFiwareConverter.fiware2Obj(_my_json, sa, setAttr=True)
            # for i in range(len(sa.sensorData)):
            #     print sa.sensorData[i]
            #     sa.sensorData[i] = SensorData(**sa.sensorData[i])
        except Exception as identifier:
            return None

        return sa

    def findSensorById(self, _trigger_name):
        _trigger_name = _trigger_name.split(".")[0]
        for sdata in self.sensorData:
            if(sdata.sensorId == _trigger_name):
                return sdata
        return None
