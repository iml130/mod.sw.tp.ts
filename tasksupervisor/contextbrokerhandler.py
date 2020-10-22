import http.client
import json
import logging
import threading
import requests

from fiwareobjectconverter.object_fiware_converter import ObjectFiwareConverter


def response_is_ok(status_code):
    if(status_code >= http.client.OK and status_code <= http.client.IM_USED):  # everything is fine
        return True
    return False


logger = logging.getLogger(__name__)

ENTITIES = "entities"
SUBSCRIPTIONS = "subscriptions"

# how to deal with "outdated" subscriptions after restart of the system
# automatic deletion of old, not needed?!
#


def convert_object_to_json_array(_obj):
    temp_array = []
    temp_array.append(_obj)
    return (temp_array)


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

    def attach_entity(self, entity):
        self.entities.append(entity)

    def register_entities(self):
        for entity in self.entities:
            self.create_entity(entity)

    def create_entity(self, entity_instance):
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

    def delete_entity(self, entity_id):
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

    def unregister_entities(self):
        for entity in range(len(self.published_entities)):
            self.delete_entity(self.published_entities[0])

    def update_entity(self, entity_instance):
        with self.lock:
            entity_id = entity_instance.id
            json_obj = ObjectFiwareConverter.obj2Fiware(
                entity_instance, ind=4, showIdValue=False)

            response = self._request("PATCH", self._getUrl(
                ENTITIES + "/" + entity_id + "/attrs"), data=json_obj, headers=self.HEADER)
            if response_is_ok(response.status_code):  # everything is fine
                logger.info("Id: %s", str(entity_instance))
                return 0

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

    def get_entities(self, _entity_id=None, _entity_type=None):

        get_url = self._getUrl(ENTITIES) + "/"
        if _entity_id:
            get_url = get_url + _entity_id
        if _entity_type:
            get_url += "?type=" + _entity_type

        response = self._request(
            "GET", get_url, headers=self.HEADER_NO_PAYLOAD)
        return json.loads(response.content.decode('utf-8'))

    def subscribe_to_entity(self, _description, _entities, _notification, _metadata=None, _expires=None, _throttling=None,
                            _condition_attributes=None, _condition_expression=None, _generic=False):
        # based upon http://telefonicaid.github.io/fiware-orion/api/v2/stable/

        with self.lock:
            subscription_id = ""
            msg = {}
            msg["description"] = _description
            has_condition = {}
            if _condition_attributes:
                has_condition["attrs"] = convert_object_to_json_array(
                    _condition_attributes)
            if _condition_expression:
                has_condition["expression"] = _condition_expression

            subject = {}
            subject["entities"] = _entities
            if _generic:
                for item in subject["entities"]:
                    item['idPattern'] = ".*"
                    del item['id']
            if has_condition:
                subject["condition"] = (has_condition)

            logger.info(str(subject))
            msg["subject"] = subject

            has_notification = {}
            if _notification:
                has_notification["http"] = {"url": _notification}

            msg["notification"] = has_notification
            subscription = {}
            if _expires:
                subscription["expires"] = _expires
            if _throttling:
                subscription["throttling"] = _throttling

            # print json.dumps(msg)
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
            return subscription_id

    def delete_subscription_by_id(self, _id):
        with self.lock:
            if len(_id) > 1:
                try:
                    # .info("Deleting Subsciption: " + id)
                    # print parsed_config_file.getFiwareServerAddress()+"/v2/subscriptions/"+ id
                    response = self._request("DELETE", self._getUrl(
                        SUBSCRIPTIONS) + "/" + _id, headers=self.HEADER_NO_PAYLOAD)
                    if response.status_code // http.client.OK == 1:
                        logger.info("Subscriptions Deleted: " + _id)
                except Exception as expression:
                    logger.info("Subscriptions Deleted FAILED: " + _id)
                    return False
                return True

    def _getUrl(self, _uri):
        return self.fiware_address + "/" + self.NGSI_VERSION + "/" + _uri

    def _getUrlv1(self):
        return self.fiware_address + "/v1/updateContext"

    def shutdown(self):
        self.unregister_entities()
