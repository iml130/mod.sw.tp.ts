import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
import requests

# local imports
from tasksupervisor.endpoint.fiware_orion.orion_interface import OrionInterface
from tasksupervisor.endpoint.fiware_orion.entities.sensor_agent_node import SensorAgent
from tasksupervisor.endpoint.fiware_orion.entities.materialflow import Materialflow
from tasksupervisor.endpoint.broker_connector import BrokerConnector
from tasksupervisor.task_supervisor_knowledge import TaskSupervisorKnowledge
from tasksupervisor.endpoint.fiware_orion.contextbrokerhandler import ContextBrokerHandler
from tasksupervisor.endpoint.fiware_orion.entities.materialflow_specification_state import MaterialflowSpecificationState
from tasksupervisor.api import materialflow_specification_state
from tasksupervisor.api import materialflow
from tasksupervisor.api import sensor_agent

from tasksupervisor import my_globals 

JSON_MATERIALFLOW_DUMMY = {
    "subscriptionId": "sub_id",
    "data": 
    [
        {
            "id": "test_id",
            "type": "Materialflow",
            "specification": {
                "value":  "specification",
                "type": "Text"
            },
            "ownerId": {
                "type": "Text",
                "value": "owner_id"
            },
            "active": {
                "type": "Boolean",
                "value": True
            }
        }
    ]
}

JSON_SENSOR_AGENT_DUMMY = {
    "subscriptionId": "sub_id",
    "data": 
    [
        {
            "id": "test_id",
            "type": "SensorAgent",
            "measurementType": {
                "type": "string",
                "value": "boolean",
                "metadata": {}
            },
            "modifiedTime": {
                "type": "string",
                "value": "formated_time",
                "metadata": {}
            },
            "readings": {
                "type": "array",
                "value": [
                    {
                        "type": "SensorReading",
                        "value": {
                            "reading": {
                                "type": "boolean",
                                "value": False
                            }
                        }
                    }
                ],
                "metadata": {}
            },
            "sanID": {
                "type": "string",
                "value": "san_id",
                "metadata": {}
            },
            "sensorID": {
                "type": "string",
                "value": "sensor_id",
                "metadata": {}
            },
            "sensorManufacturer": {
                "type": "string",
                "value": "manufacturer",
                "metadata": {}
            },
            "sensorType": {
                "type": "string",
                "value": "ON_OFF_SENSOR",
                "metadata": {}
            },
            "units": {
                "type": "string",
                "value": "boolean",
                "metadata": {}
            }
        }
    ]
}

class OptData:
    def __init__(self, description=""):
        self.description = description

class TestOrionInterface(TestCase):

    def setUp(self):
        task_supervisor_knowledge = TaskSupervisorKnowledge()
        broker_connector = BrokerConnector(task_supervisor_knowledge)
        self.orion_interface = OrionInterface(broker_connector)

    def test_subscribe_specific(self):
        sensor_agent = SensorAgent()
        context_broker_handler = self.orion_interface.context_broker_handler

        with patch.object(context_broker_handler, "subscribe_to_entity") as mock:
            self.orion_interface.subscribe(sensor_agent, generic=False)

        expected_notification = my_globals.parsed_config_file.get_taskplanner_address() + "/sensoragent"
        expected_description = "SensorAgent subscription"
        expected_entity = [{"id": sensor_agent.id, "type": "SensorAgent"}]
        mock.assert_called_with(expected_description, expected_entity, expected_notification, generic=False)

    def test_subscribe_generic(self):
        materialflow = Materialflow()
        context_broker_handler = self.orion_interface.context_broker_handler

        with patch.object(context_broker_handler, "subscribe_to_entity") as mock:
            self.orion_interface.subscribe(materialflow, generic=True)

        expected_notification = my_globals.parsed_config_file.get_taskplanner_address() + "/materialflow"
        expected_description = "Materialflow subscription"
        expected_entity = [{"id": materialflow.id, "type": "Materialflow"}]
        mock.assert_called_with(expected_description, expected_entity, expected_notification, generic=True)

    def test_subscribe_with_opt_data(self):
        materialflow = Materialflow()
        opt_data = OptData("Test Description")
        context_broker_handler = self.orion_interface.context_broker_handler

        with patch.object(context_broker_handler, "subscribe_to_entity") as mock:
            self.orion_interface.subscribe(materialflow, opt_data=opt_data, generic=True)

        expected_notification = my_globals.parsed_config_file.get_taskplanner_address() + "/materialflow"
        expected_description = opt_data.description
        expected_entity = [{"id": materialflow.id, "type": "Materialflow"}]
        mock.assert_called_with(expected_description, expected_entity, expected_notification, generic=True)

    @patch.object(ContextBrokerHandler, "subscribe_to_entity", Mock(return_value="sub_id"))
    def test_subscribe_sub_dict(self):
        materialflow = Materialflow()
        self.orion_interface.subscribe(materialflow)
        self.assertTrue("sub_id" in self.orion_interface.subscription_dict)
        self.assertEqual(self.orion_interface.subscription_dict["sub_id"], "Materialflow")

    def test_create(self):
        api_mf_spec_state = materialflow_specification_state.MaterialflowSpecificationState()
        context_broker_handler = self.orion_interface.context_broker_handler

        with patch.object(context_broker_handler, "create_entity") as mock:
            self.orion_interface.create(api_mf_spec_state)

        self.assertIsNotNone(mock.call_args)
        self.assertGreaterEqual(len(mock.call_args), 1)

        fiware_mf_spec_state = mock.call_args[0][0]
        self.assertTrue(isinstance(fiware_mf_spec_state, MaterialflowSpecificationState))

    def test_update(self):
        api_mf_spec_state = materialflow_specification_state.MaterialflowSpecificationState()
        context_broker_handler = self.orion_interface.context_broker_handler

        with patch.object(context_broker_handler, "update_entity") as mock:
            self.orion_interface.update(api_mf_spec_state)

        self.assertIsNotNone(mock.call_args)

        self.assertGreaterEqual(len(mock.call_args), 1)

        fiware_mf_spec_state = mock.call_args[0][0]
        self.assertTrue(isinstance(fiware_mf_spec_state, MaterialflowSpecificationState))
        self.assertEqual(fiware_mf_spec_state.id, str(api_mf_spec_state.id))

    def test_retreive_with_materialflow(self):
        self.orion_interface.subscription_dict["sub_id"] = "Materialflow"

        json_dummy = JSON_MATERIALFLOW_DUMMY

        with patch.object(self.orion_interface.broker_connector, "retreive") as mock:
            self.orion_interface.retreive(json_dummy)
        
        self.assertEqual(len(mock.call_args), 2)

        new_materialflow = mock.call_args[0][0]
        interface = mock.call_args[0][1]

        self.assertTrue(isinstance(new_materialflow, materialflow.Materialflow))
        self.assertEqual(new_materialflow.id, "test_id")
        self.assertEqual(new_materialflow.active, True)
        self.assertEqual(new_materialflow.specification, "specification")
        self.assertEqual(new_materialflow.owner_id, "owner_id")
        self.assertEqual(interface, self.orion_interface)

    def test_retreive_with_sensor_agent(self):
        self.orion_interface.subscription_dict["sub_id"] = "SensorAgent"

        json_dummy = JSON_SENSOR_AGENT_DUMMY

        with patch.object(self.orion_interface.broker_connector, "retreive") as mock:
            self.orion_interface.retreive(json_dummy)
        
        self.assertIsNotNone(mock.call_args)
        self.assertEqual(len(mock.call_args), 2)

        new_sensor_agent = mock.call_args[0][0]
        interface = mock.call_args[0][1]

        self.assertEqual(new_sensor_agent.id, "test_id")
        self.assertEqual(new_sensor_agent.measurement_type, "boolean")
        self.assertEqual(new_sensor_agent.modified_time, "formated_time")
        self.assertEqual(new_sensor_agent.san_id, "san_id")
        self.assertEqual(new_sensor_agent.sensor_id, "sensor_id")
        self.assertEqual(new_sensor_agent.sensor_manufacturer, "manufacturer")
        self.assertEqual(new_sensor_agent.sensor_type, "ON_OFF_SENSOR")
        self.assertEqual(new_sensor_agent.units, "boolean")
        self.assertEqual(new_sensor_agent.readings, [{"reading": False}])

if __name__ == '__main__':
    unittest.main()