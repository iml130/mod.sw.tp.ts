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

from tasksupervisor.TaskSupervisor import materialflow

# Just a plain BrokerInterface implementation to test the Connector
class TestBrokerInterface(BrokerInterface):
    def __init__(self):
        pass
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
        self.ref_owner_id = "mf_id"
        self.ref_materialflow_update_id = ""
        self._to_state_machine = DummyStateMachine()
        self._robot_id = None

class DummyMaterialflow:
    def __init__(self):
        self.taskManagerName = ""
        self.transportOrderList = []
        self.refOwnerId = "mf_id"

class TestContextBrokerHandler(TestCase):

    def setUp(self):
        self.broker_connector = BrokerConnector()
    
    def test_register_interface(self):
        test_interface = TestBrokerInterface()
        self.broker_connector.register_interface(test_interface)

        self.assertEqual(len(self.broker_connector.interfaces), 1)
        self.assertEqual(len(self.broker_connector.interface_mf_ids_dict), 1)
        self.assertEqual(len(self.broker_connector.mf_id_interface_dict), 0)

    def test_subscribe_specific(self):
        test_interface = TestBrokerInterface()
        test_interface_2 = TestBrokerInterface()

        self.broker_connector.register_interface(test_interface)
        self.broker_connector.register_interface(test_interface_2)

        with patch.object(test_interface, "subscribe") as mock:
            self.broker_connector.subscribe_specific("test_topic")
        mock.assert_called_with("test_topic", generic=False)
    
    def test_subscribe_generic(self):
        test_interface = TestBrokerInterface()
        self.broker_connector.register_interface(test_interface)
        with patch.object(test_interface, "subscribe") as mock:
            self.broker_connector.subscribe_generic("test_topic")
        mock.assert_called_with("test_topic", generic=True)
    
    def test_retreive_with_materialflow(self):
        test_interface = TestBrokerInterface()
        self.broker_connector.register_interface(test_interface)
        
        materialflow = Materialflow()
        self.broker_connector.retreive(materialflow, test_interface)

        self.assertEqual(len(self.broker_connector.interface_mf_ids_dict[test_interface]), 1)
        self.assertEqual(self.broker_connector.interface_mf_ids_dict[test_interface][0], materialflow.id)
        self.assertEqual(materialflow.id in self.broker_connector.mf_id_interface_dict, True)
        self.assertEqual(self.broker_connector.mf_id_interface_dict[materialflow.id], test_interface)
        self.assertEqual(my_globals.taskQueue.qsize(), 1)

    def test_retreive_with_sensor_agent(self):
        test_interface = TestBrokerInterface()
        self.broker_connector.register_interface(test_interface)

        sensor_agent = SensorAgent()
        self.broker_connector.retreive(sensor_agent, test_interface)
        # ToDo

    def test_create(self):
        test_interface = TestBrokerInterface()
        test_interface_2 = TestBrokerInterface()

        self.broker_connector.register_interface(test_interface)
        self.broker_connector.register_interface(test_interface_2)

        self.broker_connector.mf_id_interface_dict["mf_id"] = test_interface
        self.broker_connector.mf_id_interface_dict["mf_id_2"] = test_interface_2

        mf_spec_state = MaterialflowSpecificationState()
        mf_spec_state.refId = "mf_id"

        with patch.object(test_interface, "create") as mock:
            self.broker_connector.create(mf_spec_state)
        mock.assert_called_with(mf_spec_state)

        mf_spec_state.refId = "mf_id_2"
        with patch.object(test_interface_2, "create") as mock_2:
            self.broker_connector.create(mf_spec_state)
        mock_2.assert_called_with(mf_spec_state)

    def test_create_with_task_supervisor_info(self):
        test_interface = TestBrokerInterface()
        test_interface_2 = TestBrokerInterface()

        self.broker_connector.register_interface(test_interface)
        self.broker_connector.register_interface(test_interface_2)

        task_supervisor_info = TaskSupervisorInfo()
        self.assertIsNotNone(self.broker_connector.get_interface_by_data(task_supervisor_info))
        
        # check if methods in both interfaces are being called
        with patch.object(test_interface, "create") as mock:
            self.broker_connector.create(task_supervisor_info)
        mock.assert_called_with(task_supervisor_info)

        with patch.object(test_interface_2, "create") as mock_2:
            self.broker_connector.create(task_supervisor_info)
        mock_2.assert_called_with(task_supervisor_info)

    def test_update(self):
        test_interface = TestBrokerInterface()
        test_interface_2 = TestBrokerInterface()

        self.broker_connector.register_interface(test_interface)
        self.broker_connector.register_interface(test_interface_2)

        self.broker_connector.mf_id_interface_dict["mf_id"] = test_interface
        self.broker_connector.mf_id_interface_dict["mf_id_2"] = test_interface_2

        mf_spec_state = MaterialflowSpecificationState()
        mf_spec_state.refId = "mf_id"

        self.assertIsNotNone(self.broker_connector.get_interface_by_data(mf_spec_state))

        self.broker_connector.create(mf_spec_state)

        with patch.object(test_interface, "update") as mock:
            self.broker_connector.update(mf_spec_state)
        mock.assert_called_with(mf_spec_state)

        mf_spec_state.refId = "mf_id_2"
        self.broker_connector.create(mf_spec_state)

        with patch.object(test_interface_2, "update") as mock_2:
            self.broker_connector.update(mf_spec_state)
        mock_2.assert_called_with(mf_spec_state)
    
    def test_delete(self):
        test_interface = TestBrokerInterface()
        test_interface_2 = TestBrokerInterface()

        self.broker_connector.register_interface(test_interface)
        self.broker_connector.register_interface(test_interface_2)

        self.broker_connector.mf_id_interface_dict["mf_id"] = test_interface
        self.broker_connector.mf_id_interface_dict["mf_id_2"] = test_interface_2

        mf_spec_state = MaterialflowSpecificationState()
        mf_spec_state.refId = "mf_id"

        self.assertIsNotNone(self.broker_connector.get_interface_by_data(mf_spec_state))

        self.broker_connector.create(mf_spec_state)

        with patch.object(test_interface, "delete") as mock:
            self.broker_connector.delete(mf_spec_state)
        mock.assert_called_with(mf_spec_state)

        mf_spec_state.refId = "mf_id_2"
        self.broker_connector.create(mf_spec_state)

        with patch.object(test_interface_2, "delete") as mock_2:
            self.broker_connector.delete(mf_spec_state)
        mock_2.assert_called_with(mf_spec_state)

    def test_get_interface_by_data_with_mf_spec_state(self):
        test_interface = TestBrokerInterface()
        self.broker_connector.mf_id_interface_dict["mf_id"] = test_interface

        mf_spec_state = MaterialflowSpecificationState()
        mf_spec_state.refId = "mf_id"

        interface = self.broker_connector.get_interface_by_data(mf_spec_state)
        self.assertEqual(interface, test_interface)

    def test_get_interface_by_data_with_materialflow_update(self):
        test_interface = TestBrokerInterface()
        self.broker_connector.mf_id_interface_dict["mf_id"] = test_interface

        dummy_materialflow = DummyMaterialflow()

        materialflow_update = MaterialflowUpdate(dummy_materialflow)

        interface = self.broker_connector.get_interface_by_data(materialflow_update)
        self.assertEqual(interface, test_interface)

    def test_get_interface_by_data_with_transportorder_update(self):
        test_interface = TestBrokerInterface()
        self.broker_connector.mf_id_interface_dict["mf_id"] = test_interface

        dummy_transport_order = DummyTransportOrder()
        transport_order_update = TransportOrderUpdate(dummy_transport_order)
        transport_order_update.refOwnerId = "mf_id"

        interface = self.broker_connector.get_interface_by_data(transport_order_update)
        self.assertEqual(interface, test_interface)

if __name__ == '__main__':
    unittest.main()