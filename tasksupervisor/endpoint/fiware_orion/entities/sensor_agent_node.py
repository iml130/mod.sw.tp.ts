# using enum34
from enum import IntEnum

from tasksupervisor.endpoint.fiware_orion.entities.entity import FiwareEntity
from fiwareobjectconverter.object_fiware_converter import ObjectFiwareConverter
from tasksupervisor.api import sensor_agent

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

    def to_api_object(self):
        api_sensor_agent = sensor_agent.SensorAgent()

        api_sensor_agent.id = self.id
        api_sensor_agent.type = self.type
        api_sensor_agent.measurement_type = self.measurementType
        api_sensor_agent.modified_time = self.modifiedTime
        api_sensor_agent.readings = self.readings
        api_sensor_agent.san_id = self.sanID
        api_sensor_agent.sensor_id = self.sensorID
        api_sensor_agent.sensor_manufacturer = self.sensorManufacturer
        api_sensor_agent.sensor_type = self.sensorType
        api_sensor_agent.units = self.units

        return api_sensor_agent

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
