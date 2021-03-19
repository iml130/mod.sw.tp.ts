import http.client
import json
import logging
import threading
import requests

# third party imports
from fiwareobjectconverter.object_fiware_converter import ObjectFiwareConverter

# local imports
from tasksupervisor.endpoint.broker_connector import BrokerException

logger = logging.getLogger(__name__)

ENTITIES = "entities"
SUBSCRIPTIONS = "subscriptions"

class ContextBrokerHandler:
    lock = threading.Lock()
    HEADER = {"Content-Type": "application/json"}
    HEADER_NO_PAYLOAD = {
        "Accept": "application/json"
    }

    TIMEOUT = 1.5
    NGSI_VERSION = "v2"

    def __init__(self, fiwareAddress):
        self.fiware_address = fiwareAddress
        self.published_entities = []
        self.subscription_list = []
        self.entities = []

    def _request(self, method, url, data=None, **kwargs):
        response = None
        try:
            response = requests.request(
                method, url, data=data, headers=kwargs['headers'], timeout=self.TIMEOUT)
        except requests.exceptions.Timeout as err:
            logger.error("Orion Timeout")
            raise err
        except requests.exceptions.RequestException as err:
            logger.error(
                "except requests.exceptions.RequestException as e: %s", err)
            raise err
        except Exception as exp:
            logger.error("Orion Timeout%s", exp)
            raise exp
        return response

    def create_entity(self, entity_instance):
        with self.lock:
            logger.info("Id:" + entity_instance.id)
            status_code = http.client.OK

            json_obj = ObjectFiwareConverter.obj2Fiware(entity_instance, ind=4)
            response = self._request("POST", self._getUrl(ENTITIES), data=json_obj, headers=self.HEADER)
            status_code = response.status_code
            if not response_is_ok(status_code):
                raise BrokerException(status_code, "Unexpected HTTP status code {} received: {}".format(str(status_code), str(response.content)))
            else:
                self.published_entities.append(entity_instance.id)
    
    def delete_entity(self, entity_id):
        with self.lock:
            logger.info("Id: %s", str(entity_id))

            response = self._request("DELETE", self._getUrl(
                ENTITIES) + "/" + str(entity_id), headers=self.HEADER_NO_PAYLOAD)
            status_code = response.status_code

            if not response_is_ok(status_code):
                raise BrokerException(status_code, "Unexpected HTTP status code {} received: {}".format(str(status_code), str(response.content)))
            else:
                logger.info("Id: %s - Done", str(entity_id))
                self.published_entities.remove(entity_id)

    def update_entity(self, entity_instance):
        with self.lock:
            entity_id = entity_instance.id
            json_obj = ObjectFiwareConverter.obj2Fiware(
                entity_instance, ind=4, showIdValue=False)

            response = self._request("PATCH", self._getUrl(
                ENTITIES + "/" + entity_id + "/attrs"), data=json_obj, headers=self.HEADER)
            status_code = response.status_code
            if not response_is_ok(status_code):
                raise BrokerException(status_code, "Unexpected HTTP status code {} received: {}".format(str(status_code), str(response.content)))
            else:
                logger.info("Id: %s", str(entity_instance))

    def subscribe_to_entity(self, description, entities, notification, metadata=None, expires=None, throttling=None,
                            condition_attributes=None, condition_expression=None, generic=False):
        with self.lock:
            subscription_id = ""
            msg = {}
            msg["description"] = description
            has_condition = {}
            if condition_attributes:
                has_condition["attrs"] = convert_object_to_json_array(
                    condition_attributes)
            if condition_expression:
                has_condition["expression"] = condition_expression

            subject = {}
            subject["entities"] = entities
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

            response = self._request("POST", self._getUrl(
                SUBSCRIPTIONS), data=json.dumps(msg), headers=self.HEADER)

            subscription_id = response.headers.get('Location').replace("/v2/subscriptions/", "")
            logger.info("Subscriptions Id: %s", subscription_id)

            status_code = response.status_code
            if not response_is_ok(status_code):
                logger.info("Subscriptions Failed: %s" + str(status_code))
                raise BrokerException(status_code, "Unexpected HTTP status code {} received: {}".format(str(status_code), str(response.content)))
            else:
                logger.info("Subscriptions OK")
                self.subscription_list.append(subscription_id)
            return subscription_id

    def delete_subscription_by_id(self, id_):
        with self.lock:
            if len(id_) > 1:
                response = self._request("DELETE", self._getUrl(
                    SUBSCRIPTIONS) + "/" + id_, headers=self.HEADER_NO_PAYLOAD)
                status_code = response.status_code
                if not response_is_ok(status_code):
                    logger.info("Subscription deletion Failed: " + id_)
                    raise BrokerException(status_code, "Unexpected HTTP status code {} received: {}".format(str(status_code), str(response.content)))
                else:
                    logger.info("Subscriptions Deleted: " + id_)

    def get_entities(self, entity_id=None, entity_type=None):
        get_url = self._getUrl(ENTITIES) + "/"
        if entity_id:
            get_url = get_url + entity_id
        if entity_type:
            get_url += "?type=" + entity_type

        response = self._request("GET", get_url, headers=self.HEADER_NO_PAYLOAD)

        status_code = response.status_code
        if not response_is_ok(status_code):
            logger.info("Get entities failed: " + str(status_code))
            raise BrokerException(status_code, "Unexpected HTTP status code {} received: {}".format(str(status_code), str(response.content)))
        else:
            return json.loads(response.content.decode('utf-8'))

    def attach_entity(self, entity):
        self.entities.append(entity)

    def register_entities(self):
        for entity in self.entities:
            self.create_entity(entity)

    def unregister_entities(self):
        for entity in range(len(self.published_entities)):
            self.delete_entity(self.published_entities[0])

    def shutdown(self):
        for temp_sub_id in self.subscription_list:
            self.delete_subscription_by_id(temp_sub_id)
        self.unregister_entities()

    def _getUrl(self, uri):
        return self.fiware_address + "/" + self.NGSI_VERSION + "/" + uri

    def _getUrlv1(self):
        return self.fiware_address + "/v1/updateContext"

def response_is_ok(status_code):
    if(status_code >= http.client.OK and status_code <= http.client.IM_USED):  
        return True
    return False

def convert_object_to_json_array(obj):
    temp_array = []
    temp_array.append(obj)
    return (temp_array)
