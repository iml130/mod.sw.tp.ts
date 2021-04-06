import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
import requests

# local imports
from tasksupervisor import my_globals

from tasksupervisor.endpoint.broker_connector import BrokerConnector
from tasksupervisor.endpoint.broker_interface import BrokerInterface
from tasksupervisor.endpoint.fiware_orion.entities.materialflow import Materialflow
from tasksupervisor.endpoint.fiware_orion.entities.sensor_agent_node import SensorAgent
from tasksupervisor.endpoint.fiware_orion.entities.materialflow_specification_state import MaterialflowSpecificationState
from tasksupervisor.endpoint.fiware_orion.entities.tasksupervisor_info import TaskSupervisorInfo
from tasksupervisor.endpoint.fiware_orion.entities.transport_order_update import TransportOrderUpdate
from tasksupervisor.endpoint.fiware_orion.entities.materialflow_update import MaterialflowUpdate
from tasksupervisor.task_supervisor_knowledge import TaskSupervisorKnowledge

from tasksupervisor.TaskSupervisor import materialflow

# Just a plain BrokerInterface implementation to test the Connector
class TestBrokerInterface(BrokerInterface):
    def __init__(self, broker_id, broker_name):
        self.broker_id = broker_id
        self.broker_name = broker_name
    def start_interface(self):
        pass
    def run(self):
        pass
    def subscribe(self, topic, opt_data=None, generic=False):
        pass
    def create(self, data):
        pass
    def create(self, data):
        pass
    def update(self, data):
        pass
    def delete(self, data):
        pass
    def shutdown(self):
        pass

class DummyStateMachine:
    def __init__(self):
        self.state = None

class DummyTransportOrder:
    def __init__(self):
        self.task_name = ""
        self.start_time = None
        self._to_info = None
        self.ref_owner_id = ""
        self.broker_ref_id = "id"
        self.ref_materialflow_update_id = ""
        self._to_state_machine = DummyStateMachine()
        self._robot_id = None

class DummyMaterialflow:
    def __init__(self):
        self.taskManagerName = ""
        self.transportOrderList = []
        self.broker_ref_id = "id"

class TestContextBrokerHandler(TestCase):

    def setUp(self):
        task_supervisor_knowledge = TaskSupervisorKnowledge()
        self.broker_connector = BrokerConnector(task_supervisor_knowledge)
    
    def test_register_interface(self):
        test_interface = TestBrokerInterface("id", "broker_name")
        self.broker_connector.register_interface(test_interface)

        self.assertEqual(len(self.broker_connector.interfaces), 1)

    def test_subscribe_to_specific(self):
        test_interface = TestBrokerInterface("id", "broker_name")
        test_interface_2 = TestBrokerInterface("id_2", "broker_name_2")

        self.broker_connector.register_interface(test_interface)
        self.broker_connector.register_interface(test_interface_2)

        with patch.object(test_interface_2, "subscribe") as mock:
            self.broker_connector.subscribe_to_specific("test_topic", "id_2")
        mock.assert_called_with("test_topic", opt_data=None, generic=False)
    
    def test_subscribe_to_specific_generic(self):
        test_interface = TestBrokerInterface("id", "broker_name")
        test_interface_2 = TestBrokerInterface("id_2", "broker_name_2")

        self.broker_connector.register_interface(test_interface)
        self.broker_connector.register_interface(test_interface_2)

        with patch.object(test_interface_2, "subscribe") as mock:
            self.broker_connector.subscribe_to_specific("test_topic", "id_2", generic=True)
        mock.assert_called_with("test_topic", opt_data=None, generic=True)

    def test_subscribe_to_all(self):
        test_interface = TestBrokerInterface("id", "broker_name")
        self.broker_connector.register_interface(test_interface)
        with patch.object(test_interface, "subscribe") as mock:
            self.broker_connector.subscribe_to_all("test_topic")
        mock.assert_called_with("test_topic", opt_data=None, generic=False)
    
    def test_subscribe_to_all_generic(self):
        test_interface = TestBrokerInterface("id", "broker_name")
        self.broker_connector.register_interface(test_interface)
        with patch.object(test_interface, "subscribe") as mock:
            self.broker_connector.subscribe_to_all("test_topic", generic=True)
        mock.assert_called_with("test_topic", opt_data=None, generic=True)

    def test_retreive_with_materialflow(self):
        test_interface = TestBrokerInterface("id", "broker_name")
        self.broker_connector.register_interface(test_interface)
        
        materialflow = Materialflow()
        self.broker_connector.retreive(materialflow, test_interface)

        self.assertEqual(my_globals.taskQueue.qsize(), 1)

    def test_retreive_with_sensor_agent(self):
        test_interface = TestBrokerInterface("id", "broker_name")
        self.broker_connector.register_interface(test_interface)

        self.broker_connector.sensor_id_to_ids_dict["san_id"] = []
        self.broker_connector.sensor_id_to_ids_dict["san_id"].append("to_id")
        sensor_agent = SensorAgent()
        sensor_agent.id = "san_id"

        dict_queue = self.broker_connector.task_supervisor.sensor_dispatcher
        dict_queue.add_thread("to_id")

        self.broker_connector.retreive(sensor_agent, test_interface)
        self.assertIsNotNone(dict_queue.get_queue("to_id"))
        self.assertEqual(dict_queue.get_queue("to_id").qsize(), 1)

    def test_create(self):
        test_interface = TestBrokerInterface("id", "broker_name")
        test_interface_2 = TestBrokerInterface("id_2", "broker_name_2")

        self.broker_connector.register_interface(test_interface)
        self.broker_connector.register_interface(test_interface_2)

        mf_spec_state = MaterialflowSpecificationState()
        mf_spec_state.broker_ref_id = "id"

        with patch.object(test_interface, "create") as mock:
            self.broker_connector.create(mf_spec_state)
        mock.assert_called_with(mf_spec_state)

        mf_spec_state.broker_ref_id = "id_2"

        with patch.object(test_interface_2, "create") as mock_2:
            self.broker_connector.create(mf_spec_state)
        mock_2.assert_called_with(mf_spec_state)

    def test_create_with_task_supervisor_info(self):
        test_interface = TestBrokerInterface("id", "broker_name")
        test_interface_2 = TestBrokerInterface("id_2", "broker_name_2")

        self.broker_connector.register_interface(test_interface)
        self.broker_connector.register_interface(test_interface_2)

        task_supervisor_info = TaskSupervisorInfo()
        
        # check if methods in both interfaces are being called
        with patch.object(test_interface, "create") as mock:
            self.broker_connector.create(task_supervisor_info)
        mock.assert_called_with(task_supervisor_info)

        with patch.object(test_interface_2, "create") as mock_2:
            self.broker_connector.create(task_supervisor_info)
        mock_2.assert_called_with(task_supervisor_info)

    def test_update(self):
        test_interface = TestBrokerInterface("id", "broker_name")
        test_interface_2 = TestBrokerInterface("id_2", "broker_name_2")

        self.broker_connector.register_interface(test_interface)
        self.broker_connector.register_interface(test_interface_2)

        mf_spec_state = MaterialflowSpecificationState()
        mf_spec_state.broker_ref_id = "id"

        self.broker_connector.create(mf_spec_state)

        with patch.object(test_interface, "update") as mock:
            self.broker_connector.update(mf_spec_state)
        mock.assert_called_with(mf_spec_state)

        mf_spec_state.broker_ref_id = "id_2"
        self.broker_connector.create(mf_spec_state)

        with patch.object(test_interface_2, "update") as mock_2:
            self.broker_connector.update(mf_spec_state)
        mock_2.assert_called_with(mf_spec_state)
    
    def test_delete_with_entity(self):
        test_interface = TestBrokerInterface("id", "broker_name")
        test_interface_2 = TestBrokerInterface("id_2", "broker_name_2")

        self.broker_connector.register_interface(test_interface)
        self.broker_connector.register_interface(test_interface_2)

        with patch.object(test_interface, "delete") as mock:
            self.broker_connector.delete("entity_id", "id")
        mock.assert_called_with("entity_id", delete_entity=True)

        with patch.object(test_interface_2, "delete") as mock_2:
            self.broker_connector.delete("entity_id", "id_2")
        mock_2.assert_called_with("entity_id", delete_entity=True)

    def test_delete_with_subscription(self):
        test_interface = TestBrokerInterface("id", "broker_name")
        test_interface_2 = TestBrokerInterface("id_2", "broker_name_2")

        self.broker_connector.register_interface(test_interface)
        self.broker_connector.register_interface(test_interface_2)

        with patch.object(test_interface, "delete") as mock:
            self.broker_connector.delete("sub_id", "id", delete_entity=False)
        mock.assert_called_with("sub_id", delete_entity=False)

        with patch.object(test_interface_2, "delete") as mock_2:
            self.broker_connector.delete("sub_id", "id_2" ,delete_entity=False)
        mock_2.assert_called_with("sub_id", delete_entity=False)

    def get_interface_by_broker_id(self):
        test_interface = TestBrokerInterface("id", "broker_name")

        interface_id = self.broker_connector.get_interface_by_broker_id("id")
        self.assertEqual(interface_id, test_interface.broker_id)

if __name__ == '__main__':
    unittest.main()