""" Contains TestContextBrokerHandler TestCase """

import http
import json
import jsonschema
import unittest
from unittest import TestCase
import requests

# local imports
from tasksupervisor.endpoint.fiware_orion.contextbrokerhandler import ContextBrokerHandler
from tasksupervisor.endpoint.fiware_orion.contextbrokerhandler import BrokerException
from tasksupervisor.endpoint.fiware_orion.entities.materialflow import Materialflow

FIWARE_ADDRESS = "http://orion:1026"
ENTITY_ADDRESS = FIWARE_ADDRESS + "/v2/entities"
SUBSCRIPTION_ADDRESS = FIWARE_ADDRESS + "/v2/subscriptions"

class TestContextBrokerHandler(TestCase):
    """ Integration TestCase for the (Orion) ContextBrokerHandler """
    def setUp(self):
        self.context_broker_handler = ContextBrokerHandler(FIWARE_ADDRESS)

    def tearDown(self):
        # If we test delete_subscription_by_id subscription is already deleted
        # Catch this exception and do nothing
        try:
            self.context_broker_handler.shutdown()
        except BrokerException:
            pass

    def validate_schema(self, entity, schema):
        try:
            jsonschema.validate(entity, schema)
        except jsonschema.ValidationError as err:
            self.fail("ValidationError: " + str(err.message))
        except jsonschema.SchemaError as err:
            self.fail("SchemaError: " + str(err.message))
        except:
            self.fail("GeneralError")

    def test_create_entity(self):
        test_entitiy = Materialflow()
        self.context_broker_handler.create_entity(test_entitiy)
        response = requests.request("GET", ENTITY_ADDRESS)

        self.assertEqual(response_is_ok(response.status_code), True)

        content = json.loads(response.content.decode("utf-8"))
        materialflow_schema = open("./tasksupervisor/endpoint/fiware_orion/flask/materialflow_schema.json")

        self.validate_schema(content[0], json.loads(materialflow_schema.read()))
        materialflow_schema.close()

    def test_delete_entity(self):
        test_entity = Materialflow()

        self.assertRaises(BrokerException, self.context_broker_handler.delete_entity, test_entity.id)

        self.context_broker_handler.create_entity(test_entity)
        try:
            self.context_broker_handler.delete_entity(test_entity.id)
        except BrokerException as brokerException:
            self.fail("Fail")

        response = requests.request("GET", ENTITY_ADDRESS)
        self.assertEqual(response_is_ok(response.status_code), True)

        content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(content, [])

    def test_update_entity(self):
        test_entity = Materialflow()
        self.context_broker_handler.create_entity(test_entity)

        response = requests.request("GET", ENTITY_ADDRESS)
        self.assertEqual(response_is_ok(response.status_code), True)

        content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(content[0]["active"]["value"], False)

        test_entity.active = True
        self.context_broker_handler.update_entity(test_entity)

        response = requests.request("GET", ENTITY_ADDRESS)
        self.assertEqual(response_is_ok(response.status_code), True)

        content = json.loads(response.content.decode("utf-8"))
        self.assertEqual(content[0]["active"]["value"], True)

    def test_subscribe_to_entity(self):
        sub_id = self.context_broker_handler.subscribe_to_entity("test", [{"id": "id", "type": "type"}], FIWARE_ADDRESS)
        response = requests.request("GET", SUBSCRIPTION_ADDRESS)
        self.assertEqual(response_is_ok(response.status_code), True)
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content), 1)
        self.assertEqual(content[0]["id"], sub_id)

    def test_get_entities_with_id(self):
        test_entity = Materialflow()
        test_entity_2 = Materialflow()

        self.context_broker_handler.create_entity(test_entity)
        self.context_broker_handler.create_entity(test_entity_2)

        entity = self.context_broker_handler.get_entities(entity_id=test_entity.id)
        self.assertEqual(entity["id"], test_entity.id)

        entity = self.context_broker_handler.get_entities(entity_id=test_entity_2.id)
        self.assertEqual(entity["id"], test_entity_2.id)

    def test_get_entities_with_type(self):
        test_entity = Materialflow()
        test_entity_2 = Materialflow()

        self.context_broker_handler.create_entity(test_entity)
        self.context_broker_handler.create_entity(test_entity_2)

        entities = self.context_broker_handler.get_entities(entity_type="Materialflow")

        self.assertEqual(len(entities), 2)
        self.assertEqual(entities[0]["id"], test_entity.id)
        self.assertEqual(entities[1]["id"], test_entity_2.id)

    def test_delete_subscription_by_id(self):
        sub_id = self.context_broker_handler.subscribe_to_entity("test", [{"id": "id", "type": "type"}], FIWARE_ADDRESS)
        self.context_broker_handler.delete_subscription_by_id(sub_id)

        response = requests.request("GET", SUBSCRIPTION_ADDRESS)
        self.assertEqual(response_is_ok(response.status_code), True)
        content = json.loads(response.content.decode("utf-8"))

        self.assertEqual(len(content), 0)

def response_is_ok(status_code):
    if(status_code >= http.client.OK and status_code <= http.client.IM_USED): 
        return True
    return False

if __name__ == "__main__":
    unittest.main()
