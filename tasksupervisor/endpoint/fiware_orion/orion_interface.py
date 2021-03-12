import sys

import threading
from threading import Thread
import http.client
import json
import logging
import requests
import tasksupervisor.my_globals as my_globals 

# import local libs
from tasksupervisor.endpoint.broker_interface import BrokerInterface
from tasksupervisor.flask_setup import create_flask_app
from tasksupervisor.endpoint.broker_connector import BrokerConnector
from tasksupervisor.helpers.config_reader import ConfigReader
from tasksupervisor.api.materialflow import Materialflow
from tasksupervisor.endpoint.fiware_orion.entities import materialflow

from tasksupervisor.__main__ import callback_new_materialflow

logger = logging.getLogger(__name__)


def response_is_ok(status_code):
    if(status_code >= http.client.OK and status_code <= http.client.IM_USED):  # everything is fine
        return True
    return False

ENTITIES = "entities"
SUBSCRIPTIONS = "subscriptions"

def convert_object_to_json_array(_obj):
    temp_array = []
    temp_array.append(_obj)
    return (temp_array)

class OrionInterface(BrokerInterface):
    """ Implements the BrokerInterface for the Orion Context Broker """

    lock = threading.Lock()
    HEADER = {"Content-Type": "application/json"}
    HEADER_NO_PAYLOAD = {
        "Accept": "application/json"
    }

    TIMEOUT = 1.5
    NGSI_VERSION = "v2"

    def __init__(self, fiware_address, tasksupervisor_knowledge, broker_connector):
        threading.Thread.__init__(self)
        self.fiware_address = fiware_address
        self.published_entities = []
        self.subscription_list = []
        self.entities = []
        self.tasksupervisor_knowledge = tasksupervisor_knowledge
        self.subscription_dict = {}
        self.broker_connector = broker_connector
    
    def run(self):
        app = create_flask_app(self.tasksupervisor_knowledge, self)
        app.run(host=my_globals.parsed_config_file.FLASK_HOST,
                port=my_globals.parsed_config_file.TASKPLANNER_PORT,
                threaded=True, use_reloader=False, debug=True)

    def subscribe(self, topic, opt_data = None):
        description = ""
        generic = True
        notification = ""
        metadata = None
        expires = None
        throttling = None
        condition_attributes = None
        condition_expression = None
        entity_type = ""

        class_name = str(topic.__class__.__name__)
        if class_name == "Materialflow":
            description = "Materialflow subscription"
            notification = my_globals.parsed_config_file.get_taskplanner_address() + "/materialflow"
            entity_type = "Materialflow"
        elif class_name == "SensorAgent":
            if opt_data and str(opt_data.__class__.__name__) == "TransportOrder":
                transport_order = opt_data
                notification = self.tasksupervisor_knowledge.task_planner_address + "/san/" + transport_order.id
            else:
                print("Wrong data in opt_data in subscribe: " + opt_data)
        else:
            print("Error while subscribing: Unknown class " + class_name)

        with self.lock:
            subscription_id = ""
            msg = {}
            msg["description"] = description
            has_condition = {}

            condition_attributes = None
            condition_expression = None
            if condition_attributes:
                has_condition["attrs"] = convert_object_to_json_array(
                    _condition_attributes)
            if condition_expression:
                has_condition["expression"] = condition_expression

            subject = {}
            subject["entities"] = [{"id": topic.id, "type": str(topic.__class__.__name__)}]

            if generic:
                for item in subject["entities"]:
                    item['idPattern'] = ".*"
                    del item['id']
            if has_condition:
                subject["condition"] = (has_condition)

            logger.info(str(subject))
            msg["subject"] = subject

            has_notification = {}
            if notification:
                has_notification["http"] = {"url": notification}

            msg["notification"] = has_notification
            subscription = {}

            if expires:
                subscription["expires"] = expires
            if throttling:
                subscription["throttling"] = throttling

            try:
                #response = requests.post(self._getUrl(SUBSCRIPTIONS), data=json.dumps(msg), headers= self.HEADERS, timeout = self.TIMEOUT)
                print(json.dumps(msg))
                response = self._request("POST", self._getUrl(
                    SUBSCRIPTIONS), data=json.dumps(msg), headers=self.HEADER)

                subscription_id = response.headers.get(
                    'Location').replace("/v2/subscriptions/", "")
                logger.info("Subscriptions Id: %s", subscription_id)

            except requests.exceptions.Timeout:
                pass

            status_code = response.status_code
            if response_is_ok(status_code):  # everything is fine
                logger.info("Subscriptions OK")
                self.subscription_list.append(subscription_id)

            else:
                logger.info("Subscriptions Failed: %s" + status_code)
           
            self.subscription_dict[subscription_id] = entity_type

    def create(self, data):
        with self.lock:
            logger.info("Id:" + entity_instance.id)
            status_code = http.client.OK

            # check maybe to delete:
            # if(self.delete_entity(entity_instance.getId())):
            #     print "error"

            json_obj = ObjectFiwareConverter.obj2Fiware(entity_instance, ind=4)
            try:
                response = self._request("POST", self._getUrl(
                    ENTITIES), data=json_obj, headers=self.HEADER)
                status_code = response.status_code
                if not response_is_ok(status_code):
                    return json.loads(response.content)
                else:
                    self.published_entities.append(entity_instance.id)
                    return 0
                    # todo: raise error
            except:
                logger.error("No Connection to Orion :(")
                return -1

    def update(self, data):
        with self.lock:
            entity_id = entity_instance.id
            json_obj = ObjectFiwareConverter.obj2Fiware(
                entity_instance, ind=4, showIdValue=False)

            response = self._request("PATCH", self._getUrl(
                ENTITIES + "/" + entity_id + "/attrs"), data=json_obj, headers=self.HEADER)
            if response_is_ok(response.status_code):  # everything is fine
                logger.info("Id: %s", str(entity_instance))
                return 0

    def delete(self, data):
        with self.lock:
            logger.info("Id: %s", str(entity_id))

            response = self._request("DELETE", self._getUrl(
                ENTITIES) + "/" + str(entity_id), headers=self.HEADER_NO_PAYLOAD)
            status_code = response.status_code

            if response_is_ok(status_code):  # everything is fine
                logger.info("Id: %s - Done", str(entity_id))

                self.published_entities.remove(entity_id)
                return 0
            else:
                #content = json.loads(response.content)

                return status_code

    def retreive(self, json_requests):
        subscription_id = json_requests[my_globals.FI_SUB_ID]
        entity_type = self.subscription_dict[subscription_id]
        if entity_type == "Materialflow":
            # it might be possible that there are multiple entities
            # iterate over each json request
            for temp_json_request in json_requests[my_globals.FI_DATA]:
                # create an entity from the json request
                orion_materialflow = materialflow.Materialflow.CreateObjectFromJson(
                    temp_json_request)

                api_materialflow = orion_materialflow.to_api_object()
                broker_connector.retreive(api_materialflow, self)

    def schema_valid(self, data):
        pass

    def _request(self, method, url, data=None, **kwargs):
        response = None
        try:
            response = requests.request(
                method, url, data=data, headers=kwargs['headers'], timeout=self.TIMEOUT)
        except requests.exceptions.Timeout:
            logger.error("Orion Timeout :(")
        except requests.exceptions.RequestException as err:
            logger.error(
                "except requests.exceptions.RequestException as e: %s", err)
        except Exception as exp:
            logger.error("Orion Timeout :( %s", exp)
        return response

    def _getUrl(self, _uri):
        return self.fiware_address + "/" + self.NGSI_VERSION + "/" + _uri

    def _getUrlv1(self):
        return self.fiware_address + "/v1/updateContext"

    def shutdown(self):
        self.unregister_entities()

    def unregister_entities(self):
        for entity in range(len(self.published_entities)):
            self.delete_entity(self.published_entities[0])


if __name__ == "__main__":
    CONFIG_FILE = "./tasksupervisor/fiware_config.ini"

    try:
        parsed_config_file = ConfigReader(CONFIG_FILE)
        parsed_config_file.is_valid()
    except Exception:
        sys.exit(0)
    
    broker_connector = BrokerConnector()

    interface = OrionInterface(parsed_config_file.get_fiware_server_address(), None, broker_connector)

    broker_connector.register_interface(interface)
    interface.start()

    thread_new_materialflow = Thread(target=callback_new_materialflow,
                                     args=(my_globals.taskQueue, None))
    thread_new_materialflow.start()

    new_materialflow = Materialflow()
    broker_connector.subscribe_generic(new_materialflow)