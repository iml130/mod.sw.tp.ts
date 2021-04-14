import os
import http
import threading
import json
import jsonschema
import unittest
import time
from unittest import TestCase
import requests

from tasksupervisor.helpers import servercheck
from tasksupervisor.endpoint.fiware_orion.orion_interface import OrionInterface
from tasksupervisor.endpoint.fiware_orion.flask.flask_setup import create_flask_app

from tasksupervisor.endpoint.fiware_orion.contextbrokerhandler import ContextBrokerHandler
from tasksupervisor.endpoint.fiware_orion.entities.materialflow import Materialflow
from tasksupervisor.endpoint.fiware_orion.entities.sensor_agent_node import SensorAgent

FLASK_HOST = "0.0.0.0"
FLASK_PORT = 2906

ORION_PORT = 1026

# Host names used here are for testing with github actions only
FIWARE_ADDRESS = "http://orion:1026"
ENTITY_ADDRESS = FIWARE_ADDRESS + "/v2/entities"

SUPERVISOR_ADDRESS = "http://integration-test:2906"

HEADER = {"Content-Type": "application/json"}
HEADER_NO_PAYLOAD = {
    "Accept": "application/json"
}

MF_DUMMY = {
	"id": "mf_id",
	"type": "Materialflow",
	"specification": {
		"value":  "mf_specification",
		"type": "Text"
	},
	"ownerId": {
		"type": "Text",
		"value": "reviewers hmi"
	},
	"active": {
		"type": "Boolean",
		"value": True
	}
}

SENSOR_DUMMY = {
    "id": "sensor_id",
    "type": "SensorAgent",
    "measurementType": {
        "type": "string",
        "value": "boolean",
        "metadata": {}
    },
    "modifiedTime": {
        "type": "string",
        "value": "2019-09-11T09:36:53Z",
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
        "value": "SAN1",
        "metadata": {}
    },
    "sensorID": {
        "type": "string",
        "value": "AUniqueNameforAButton",
        "metadata": {}
    },
    "sensorManufacturer": {
        "type": "string",
        "value": "LLC",
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

def callback_flask_server(flask_app):
    flask_app.run(host=FLASK_HOST,
                  port=FLASK_PORT,
                  threaded=True, use_reloader=False, debug=True)

class DummyInterface():
    def __init__(self):
        self.data = ""
    def retreive(self, data):
        self.data = data

class TestOrionEndpoints(TestCase):
    """ Integration TestCase for the (Orion) ContextBrokerHandler """

    @classmethod
    def setUpClass(cls):
        cls.dummy_interface = DummyInterface()
        cls.app = create_flask_app(cls.dummy_interface)

        thread_flask_server = threading.Thread(name="callback_flask_server", target=callback_flask_server,
                                                    args=(cls.app,))
        thread_flask_server.setDaemon(True) # Terminate when main thread terminates
        thread_flask_server.start()

        cls.context_broker_handler = ContextBrokerHandler(FIWARE_ADDRESS)

    def tearDown(self):
        TestOrionEndpoints.context_broker_handler.shutdown()
        requests.request("DELETE", ENTITY_ADDRESS + "/" + str("mf_id"), headers=HEADER_NO_PAYLOAD)
        requests.request("DELETE", ENTITY_ADDRESS + "/" + str("sensor_id"), headers=HEADER_NO_PAYLOAD) 

    def test_materialflow_endpoint(self):
        topic = Materialflow()
        entities = [{"id": topic.id, "type": "Materialflow"}]
        notification = SUPERVISOR_ADDRESS + "/materialflow"
        TestOrionEndpoints.context_broker_handler.subscribe_to_entity("description", entities,
                                                                 notification, generic=True)
        time.sleep(3)
        requests.request("POST", ENTITY_ADDRESS, data=json.dumps(MF_DUMMY), headers=HEADER)
        time.sleep(3)

        interface_data = TestOrionEndpoints.dummy_interface.data

        self.assertIsInstance(interface_data, dict)
        self.assertTrue("data" in interface_data)
        self.assertEqual(len(interface_data["data"]), 1)
        self.assertTrue("id" in interface_data["data"][0])
        self.assertEqual(interface_data["data"][0]["id"], "mf_id")

    def test_sensor_agent_endpoint(self):
        topic = SensorAgent("sensor_id")
        entities = [{"id": topic.id, "type": "SensorAgent"}]
        notification = SUPERVISOR_ADDRESS + "/san/to_id"
        TestOrionEndpoints.context_broker_handler.subscribe_to_entity("description", entities,
                                                                 notification, generic=False)
        time.sleep(3)
        requests.request("POST", ENTITY_ADDRESS, data=json.dumps(SENSOR_DUMMY), headers=HEADER)
        time.sleep(3)

        interface_data = TestOrionEndpoints.dummy_interface.data

        self.assertIsInstance(interface_data, dict)
        self.assertTrue("data" in interface_data)
        self.assertEqual(len(interface_data["data"]), 1)
        self.assertTrue("id" in interface_data["data"][0])
        self.assertEqual(interface_data["data"][0]["id"], "sensor_id")

if __name__ == "__main__":
    unittest.main()
