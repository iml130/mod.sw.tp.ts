import ast
import logging

from tasksupervisor.entities.sensor_agent_node import SensorAgent

logger = logging.getLogger(__name__)


COMPARISON_OPERATOR_EQUAL = "=="
COMPARISON_OPERATOR_NOT_EQUAL = "!="
COMPARISON_OPERATOR_LESS_THAN = "<"
COMPARISON_OPERATOR_GREATER_THAN = ">"
COMPARISON_OPERATOR_LESS_OR_EQUAL_THAN = "<="
COMPARISON_OPERATOR_GREATER_OR_EQUAL_THAN = ">="


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


def checkIfSensorEventTriggersNextTransportUpdate(sensor_entity_data, sub_ids, expected_value, expected_type, expected_comperator):
    if sensor_entity_data:
        if "subscriptionId" in sensor_entity_data:

            if sensor_entity_data["subscriptionId"] in sub_ids:
                for sensor_data in sensor_entity_data["data"]:
                    dd = SensorAgent.CreateObjectFromJson(sensor_data)
                    if expected_value:
                        if dd.readings:
                            if expected_type:
                                if validate_event(dd.readings, expected_value, expected_type, expected_comperator):
                                    return True
    return False


def validate_event(sensor_data, expected_value, expected_type, expected_comperator):
    return_code, actual_type = check_for_type(expected_type, sensor_data)
    if return_code:
        return check_for_value(actual_type, sensor_data, expected_value, expected_comperator)
        # expected value is true, now check if the real value is also correct


def check_for_value(actual_type, real_value, expected_value, expected_comperator):

    received_value = real_value[0]["reading"]
    #received_value = False
    # print(type(expected_value))
    # print(ast.literal_eval(expected_value))
    compare_operator = expected_comperator
    logger.info("received_value: %s,  expectedValue: %s",
                str(received_value), str(expected_value))

    if actual_type >= 0 and actual_type <= 2:
        # 0 = boolean, 1 = integer, 2 = float
        return_value = False
        if compare_operator == COMPARISON_OPERATOR_EQUAL:  # equal
            return_value = (ast.literal_eval(expected_value) == received_value)
        elif compare_operator == COMPARISON_OPERATOR_GREATER_THAN:  # greater
            return_value = (received_value > ast.literal_eval(expected_value))
        elif compare_operator == COMPARISON_OPERATOR_LESS_THAN:  # less than
            return_value = (received_value > ast.literal_eval(expected_value))
        elif compare_operator == COMPARISON_OPERATOR_GREATER_OR_EQUAL_THAN:  # greater than or equal
            return_value = (received_value >= ast.literal_eval(expected_value))
        elif compare_operator == COMPARISON_OPERATOR_LESS_OR_EQUAL_THAN:  # less than or equal
            return_value = (received_value <= ast.literal_eval(expected_value))
        elif compare_operator == COMPARISON_OPERATOR_NOT_EQUAL:  # not euqal
            return_value = (ast.literal_eval(expected_value) != received_value)
        return return_value
        # boolean

    elif actual_type == 3:
        # str
        pass
    pass


def check_for_type(expected_type, sensor_data):
    expected_type = expected_type.lower()
    sensor_reading_type = sensor_data[0]["reading"]
    if expected_type == "boolean" or expected_type == "bool":
        if isinstance(sensor_reading_type, bool):
            logger.info("expected_type: %s, receivedType: Bool",
                        str(expected_type))
            return True, 0
    elif expected_type == "integer" or expected_type == "int":
        if isinstance(sensor_reading_type, int):
            logger.info("expected_type: %i, receivedType: Float",
                        expected_type)
            return True, 1
    elif expected_type == "float":
        if isinstance(sensor_reading_type, float):
            logger.info("expected_type: %s, receivedType: Float",
                        expected_type)
            return True, 2
    elif expected_type == "str":
        if isinstance(sensor_reading_type, str):
            logger.info("expected_type: %s, receivedType: Str", expected_type)
            return True, 3
    return False, None
