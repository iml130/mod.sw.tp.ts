import requests
import json 
import httplib

from FiwareObjectConverter.objectFiwareConverter import ObjectFiwareConverter

def isResponseOk(statusCode):
    if(statusCode >= httplib.OK and statusCode <= httplib.IM_USED): # everything is fine
        return True
    return False


ENTITIES = "entities"
SUBSCRIPTIONS = "subscriptions"

def obj2JsonArray(_obj):
    tempArray = []
    tempArray.append(_obj)
    return (tempArray)

class ContextBrokerHandler:
    HEADER = {"Content-Type" : "application/json"}
    HEADER_NO_PAYLOAD = {
        "Accept": "application/json"
    }

    TIMEOUT = 0.5
    NGSI_VERSION = "v2"

    def __init__(self, fiwareAddress):
        self.fiwareAddress = fiwareAddress 
        self.published_entities = []
        self.entities = []

    def attach_entity(self, entity):
        self.entities.append(entity)

    def register_entities(self):
        for entity in self.entities:
            self.create_entity(entity)

    def create_entity(self, entityInstance):
        print "Create Entity"
        statusCode = httplib.OK

        # check maybe to delete:
        if(self.delete_entity(entityInstance.getId())):
            print "error"

        json = ObjectFiwareConverter.obj2Fiware(entityInstance, ind=4)     
        response = self._request("POST",self._getUrl(ENTITIES), data = json, headers = self.HEADER)
        statusCode = response.status_code
        if(not isResponseOk(statusCode)):
            return json.loads(response.content)
            # todo: raise error 

    def delete_entity(self, entityId):
        print "Delete Entity - Id: " + str (entityId) 
        response = self._request("DELETE", self._getUrl(ENTITIES) + "/" + str(entityId), headers = self.HEADER_NO_PAYLOAD)
        statusCode = response.status_code
        
        if(isResponseOk(statusCode)): # everything is fine
            print "Status OK"
            return 0
        else:
            content = json.loads(response.content)
            print content
            return statusCode

    def unregister_entities(self):
        for entity in self.published_entities:
            self.delete_entity(entity)
            self.published_entities.remove(entity)

    def update_entity(self, entityInstance):
        json = ObjectFiwareConverter.obj2Fiware(entityInstance, ind=4, showIdValue= False)     
        response = self._request("PATCH",self._getUrl(ENTITIES +"/"+  entityInstance.getId() + "/attrs"), data = json, headers = self.HEADER) 
        if(isResponseOk(response.status_code)): #everything is fine
            print "Status OK"
            return 0
    
    def update_entity_dirty(self, _json):
        response = self._request("POST",self._getUrlv1(), data = _json, headers = self.HEADER) 
        if(isResponseOk(response.status_code)): #everything is fine
            print "Status OK"
            return 0

    # def subscribe(self, msg, subscriber):
    #     self.subscribers.setdefault(msg, []).append(subscriber)

    # def unsubscribe(self, msg, subscriber):
    #     self.subscribers[msg].remove(subscriber)

    # def update(self):
    #     for msg in self.msg_queue:
    #         for sub in self.subscribers.get(msg, []):
    #             sub.run(msg)
    #     self.msg_queue = []
 
    def _request(self, method, url, data = None, **kwargs):
        response = None
        try:           
            response = requests.request(method, url, data = data, headers = kwargs['headers'], timeout = self.TIMEOUT)      
        except requests.exceptions.Timeout:
            print "pass"
        return response

    def getEntities(self, _entityId = None , _entityType=None):
        
        getUrl = self._getUrl(ENTITIES) + "/"
        if (_entityId):
            getUrl = getUrl + _entityId
        if (_entityType):
            getUrl += "?type=" + _entityType
        
        response = self._request("GET", getUrl, headers = self.HEADER_NO_PAYLOAD)
        return json.loads(response.content.decode('utf-8'))

    def subscribe2Entity(self, _description, _entities, _notification,  _metadata=None, _expires=None, _throttling=None,
                        _condition_attributes=None, _condition_expression=None):
        # based upon http://telefonicaid.github.io/fiware-orion/api/v2/stable/

        msg = {}
        msg["description"] = _description
        condition = {}
        if _condition_attributes:
            condition["attrs"] = obj2JsonArray(_condition_attributes)
        if _condition_expression:
            condition["expression"] = _condition_expression

        subject = {}
        subject["entities"] = _entities
        if(condition):
            subject["condition"]  = (condition)
        print condition
        print subject
        msg["subject"] = subject

        notification = {}
        if _notification:
            notification["http"] = { "url" : _notification}

        msg["notification"] = notification
        if _expires:
            subscription["expires"] = _expires
        if _throttling:
            subscription["throttling"] = _throttling

        print json.dumps(msg) 
        try:            
            #response = requests.post(self._getUrl(SUBSCRIPTIONS), data=json.dumps(msg), headers= self.HEADERS, timeout = self.TIMEOUT)
            response = self._request("POST",self._getUrl(SUBSCRIPTIONS), data =json.dumps(msg), headers = self.HEADER)
            print response.headers.get('Location')

        except requests.exceptions.Timeout:
            pass
               
        statusCode = response.status_code
        if(isResponseOk(statusCode)): # everything is fine 
            print "Status OK"            
        return response.headers.get('Location').replace("/v2/subscriptions/","")

    def _getUrl(self, _uri):
        return (self.fiwareAddress + "/" + self.NGSI_VERSION + "/" + _uri)

    def _getUrlv1(self):
        return (self.fiwareAddress + "/v1/updateContext")       