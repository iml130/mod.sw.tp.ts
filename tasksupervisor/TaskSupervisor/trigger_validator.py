import ast
import logging

from tasksupervisor.entities.sensor_agent_node import SensorAgent

logger = logging.getLogger(__name__)

def get_sensor_physical_sensor_name(sensor_entity_data, sub_ids):
    if sensor_entity_data:
        if "subscriptionId" in sensor_entity_data:

            if sensor_entity_data["subscriptionId"] in sub_ids:
                for sensor_data in sensor_entity_data["data"]:
                    dd = SensorAgent.CreateObjectFromJson(sensor_data)
                    if dd:
                        return dd.sensorID
    return NotImplementedError


def get_sensor_value(sensor_entity_data, sub_ids):
    if sensor_entity_data:
        if "subscriptionId" in sensor_entity_data:
            if sensor_entity_data["subscriptionId"] in sub_ids:
                for sensor_data in sensor_entity_data["data"]:
                    dd = SensorAgent.CreateObjectFromJson(sensor_data)
                    if dd.readings:
                        return dd.readings[0]["reading"]
    return None
