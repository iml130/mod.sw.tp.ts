import unittest
from unittest import TestCase
from unittest.mock import Mock, patch
import requests

# local imports
from tasksupervisor.endpoint.fiware_orion.contextbrokerhandler import ContextBrokerHandler
from tasksupervisor.endpoint.fiware_orion.contextbrokerhandler import BrokerException 
from tasksupervisor.endpoint.fiware_orion.entities.materialflow import Materialflow

FIWARE_ADDRESS = "http://127.0.0.1:1026"
TEST_HEADER = {"Content-Type": "application/json"}

class TestResponse:
    def __init__(self, content, status_code=None, headers=None):
        self.content = content.encode("utf-8")
        self.status_code = status_code
        self.headers = headers

class TestContextBrokerHandler(TestCase):

    def setUp(self):
        self.context_broker_handler = ContextBrokerHandler(FIWARE_ADDRESS)

    """
        _request tests
    """
    @patch.object(requests, "request", Mock(side_effect=requests.exceptions.Timeout))
    def test_request_with_timeout_exception(self):
        self.assertRaises(requests.exceptions.Timeout, self.context_broker_handler._request, "POST", "url", headers=TEST_HEADER)

    @patch.object(requests, "request", Mock(side_effect=requests.exceptions.RequestException))
    def test_request_with_request_exception(self):
        self.assertRaises(requests.exceptions.RequestException, self.context_broker_handler._request, "POST", "url", headers=TEST_HEADER)

    @patch.object(requests, "request", Mock(side_effect=Exception))
    def test_request_with_exception(self):
        self.assertRaises(Exception, self.context_broker_handler._request, "POST", "url", headers=TEST_HEADER)

    """ 
        create_entity tests
    """
    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 500,
        content = "Error"
    )))
    def test_create_entity_with_error(self):
        test_entitiy = Materialflow()
        self.assertRaises(BrokerException, self.context_broker_handler.create_entity, test_entitiy)

    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 200, #http.client.OK
        content = "No error"
    )))
    def test_create_entity_without_error(self):
        test_entity = Materialflow()
        try:
            self.context_broker_handler.create_entity(test_entity)
        except Exception:
            self.fail("create_entity raised an Exception which should not happen!")

    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 200,
        content = "No error"
    )))
    def test_create_entity_creation(self):
        test_entity = Materialflow()
        self.context_broker_handler.create_entity(test_entity)
        self.assertEqual(len(self.context_broker_handler.published_entities), 1)

    """
        delete_entity tests
    """
    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 500,
        content = "Error"
    )))
    def test_delete_entity_with_error(self):
        test_entitiy = Materialflow()
        self.assertRaises(BrokerException, self.context_broker_handler.create_entity, test_entitiy)

    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 200,
        content = "No error"
    )))
    def test_delete_entity_without_error(self):
        test_entitiy = Materialflow()
        try:
            self.context_broker_handler.published_entities.append("uuid")
            self.context_broker_handler.delete_entity("uuid")
        except Exception:
            self.fail("delete_entity raised and Exception which should not happen!")

    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 200,
        content = "No error"
    )))
    def test_delete_entity_deletion(self):
        test_entitiy = Materialflow()
        self.context_broker_handler.published_entities.append("uuid")
        self.context_broker_handler.delete_entity("uuid")
        self.assertEqual(len(self.context_broker_handler.published_entities), 0)

    """
        update_entity tests
    """
    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 500,
        content = "Error"
    )))
    def test_update_entity_with_error(self):
        test_entitiy = Materialflow()
        self.assertRaises(BrokerException, self.context_broker_handler.update_entity, test_entitiy)
    
    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 200,
        content = "No error"
    )))
    def test_update_entity_without_error(self):
        test_entitiy = Materialflow()
        try:
            self.context_broker_handler.update_entity(test_entitiy)
        except Exception:
            self.fail("update_entity raised and Exception which should not happen!")
 
    """
        subscribe entity tests
    """
    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 500,
        content = "Error",
        headers = {'Location': 'sub_id'}
    )))
    def test_subscribe_to_entity_with_error(self):
        test_entitiy = Materialflow()
        self.assertRaises(BrokerException, self.context_broker_handler.subscribe_to_entity, "", [{"id": "id", "type": "type"}], None)

    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 200,
        content = "No error",
        headers = {'Location': 'sub_id'}
    )))
    def test_subscribe_to_entity_without_error(self):
        test_entitiy = Materialflow()
        try:
            self.context_broker_handler.subscribe_to_entity("", [{"id": "id", "type": "type"}], None)
        except Exception:
            self.fail("subscribe_to_entity raised and Exception which should not happen!")

    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 200,
        content = "No error",
        headers = {'Location': 'sub_id'}
    )))
    def test_subscribe_to_entity_sub_id(self):
        test_entity = Materialflow()
        sub_id = self.context_broker_handler.subscribe_to_entity("", [{"id": "id", "type": "type"}], None)
        self.assertEqual(sub_id, "sub_id")

    """
        delete_subscription_by_id tests
    """
    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 500,
        content = "Error"
    )))
    def test_delete_subscription_by_id_with_error(self):
        self.assertRaises(BrokerException, self.context_broker_handler.delete_subscription_by_id, "sub_id")

    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 200,
        content = "No error"
    )))
    def test_delete_subscription_by_id_without_error(self):
        test_entitiy = Materialflow()
        try:
            self.context_broker_handler.delete_subscription_by_id("sub_id")
        except Exception:
            self.fail("delete_subscription_by_id raised and Exception which should not happen!")

    """
        get_entities tests
    """
    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 500,
        content = "Error"
    )))
    def test_get_entities_with_error(self):
        self.assertRaises(BrokerException, self.context_broker_handler.get_entities, "entity_id", "entitiy_type")

    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 200,
        content = '{"Entity": "test"}'
    )))
    def test_get_entities_without_error(self):
        try:
            self.context_broker_handler.get_entities("entity_id", "entitiy_type")
        except Exception:
            self.fail("Subscribe to entity raised and Exception which should not happen!")

    @patch.object(ContextBrokerHandler, "_request", Mock(return_value=TestResponse(
        status_code = 200,
        content = '{"Entity": "test"}'
    )))
    def test_get_entities_get_content(self):
        entity = self.context_broker_handler.get_entities("entity_id", "entitiy_type")
        self.assertEqual(entity, {"Entity": "test"})
