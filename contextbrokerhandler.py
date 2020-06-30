import requests
import json 
import httplib
import threading 
import logging 

from FiwareObjectConverter.objectFiwareConverter import ObjectFiwareConverter

def isResponseOk(statusCode):
    if(statusCode >= httplib.OK and statusCode <= httplib.IM_USED): # everything is fine
        return True
    return False

logger = logging.getLogger(__name__)

ENTITIES = "entities"
SUBSCRIPTIONS = "subscriptions"

# how to deal with "outdated" subscriptions after restart of the system
# automatic deletion of old, not needed?!
# 
def obj2JsonArray(_obj):
    tempArray = []
    tempArray.append(_obj)
    return (tempArray)


class ContextBrokerHandler:
    lock = threading.Lock()
    HEADER = {"Content-Type" : "application/json"}
    HEADER_NO_PAYLOAD = {
        "Accept": "application/json"
    }

    TIMEOUT = 1.5
    NGSI_VERSION = "v2"

    def __init__(self, fiwareAddress):
        self.fiwareAddress = fiwareAddress 
        self.published_entities = []
        self.listOfSubscriptions = []        
        self.entities = []

    def attach_entity(self, entity):
        self.entities.append(entity)

    def register_entities(self):
        for entity in self.entities:
            self.create_entity(entity)

    def create_entity(self, entityInstance):
        with self.lock:
            logger.info("Id:" + entityInstance.id)
            statusCode = httplib.OK

            # check maybe to delete:
            # if(self.delete_entity(entityInstance.getId())):
            #     print "error"

            jsonObj = ObjectFiwareConverter.obj2Fiware(entityInstance, ind=4)     
            try:
                response = self._request("POST",self._getUrl(ENTITIES), data = jsonObj, headers = self.HEADER)
                statusCode = response.status_code
                if(not isResponseOk(statusCode)):
                    return json.loads(response.content)
                else:
                    self.published_entities.append(entityInstance.id)
                    return 0
                    # todo: raise error 
            except Exception as e:
                logger.error("No Connection to Orion :(")
                return -1


    def delete_entity(self, entityId):
        with self.lock:
            logger.info("Id: " + str (entityId))

            response = self._request("DELETE", self._getUrl(ENTITIES) + "/" + str(entityId), headers = self.HEADER_NO_PAYLOAD)
            statusCode = response.status_code
            
            if(isResponseOk(statusCode)): # everything is fine
                logger.info("Id: " + str (entityId) + " -  Done")
                
                self.published_entities.remove(entityId)
                return 0
            else:
                content = json.loads(response.content)
                
                return statusCode

    def unregister_entities(self):         
        for entity in range(len(self.published_entities)):
            self.delete_entity(self.published_entities[0]) 

    def update_entity(self, entityInstance):
        with self.lock:
            id = entityInstance.id     
            json = ObjectFiwareConverter.obj2Fiware(entityInstance, ind=4, showIdValue = False)  
            
            response = self._request("PATCH",self._getUrl(ENTITIES +"/"+  id + "/attrs"), data = json, headers = self.HEADER) 
            if(isResponseOk(response.status_code)): #everything is fine
                logger.info("Id: " + str (entityInstance))
                return 0
    
    def _request(self, method, url, data = None, **kwargs):
        response = None
        try:           
            response = requests.request(method, url, data = data, headers = kwargs['headers'], timeout = self.TIMEOUT)      
        except requests.exceptions.Timeout:
            logger.error("Orion Timeout :(")
        except Exception as exp:
            logger.error("Orion Timeout :(" + exp.message)
        except requests.exceptions.RequestException as e:
            logger.error("except requests.exceptions.RequestException as e:" + exp.message)
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
                        _condition_attributes=None, _condition_expression=None, _generic = False):
        # based upon http://telefonicaid.github.io/fiware-orion/api/v2/stable/

        with self.lock:
            subscriptionId = ""
            msg = {}
            msg["description"] = _description
            condition = {}
            if _condition_attributes:
                condition["attrs"] = obj2JsonArray(_condition_attributes)
            if _condition_expression:
                condition["expression"] = _condition_expression

            subject = {}
            subject["entities"] = _entities
            if(_generic):
                for item in subject["entities"]:
                    item['idPattern'] = ".*"
                    del item['id']
            if(condition):
                subject["condition"]  = (condition)
            
            logger.info(str(subject))
            msg["subject"] = subject

            notification = {}
            if _notification:
                notification["http"] = { "url" : _notification}

            msg["notification"] = notification
            if _expires:
                subscription["expires"] = _expires
            if _throttling:
                subscription["throttling"] = _throttling

            #print json.dumps(msg) 
            try:            
                #response = requests.post(self._getUrl(SUBSCRIPTIONS), data=json.dumps(msg), headers= self.HEADERS, timeout = self.TIMEOUT)
                response = self._request("POST",self._getUrl(SUBSCRIPTIONS), data =json.dumps(msg), headers = self.HEADER)
                subscriptionId = response.headers.get('Location').replace("/v2/subscriptions/","")
                logger.info("Subscriptions Id: " + subscriptionId)
    

            except requests.exceptions.Timeout:
                pass
                
            statusCode = response.status_code
            if(isResponseOk(statusCode)): # everything is fine 
                logger.info("Subscriptions OK")
                self.listOfSubscriptions.append(subscriptionId)
                
            else:
                logger.info("Subscriptions Failed: " + statusCode)
            return subscriptionId

    def deleteSubscriptionById(self, id):
        with self.lock:
            if(len(id)>1):
                try:
                    #.info("Deleting Subsciption: " + id) 
                    #print parsedConfigFile.getFiwareServerAddress()+"/v2/subscriptions/"+ id
                    response = self._request("DELETE", self._getUrl(SUBSCRIPTIONS) + "/" + id , headers = self.HEADER_NO_PAYLOAD)
                    if(response.status_code // httplib.OK == 1):
                        logger.info("Subscriptions Deleted: " + id)
                except Exception as expression:
                    logger.info("Subscriptions Deleted FAILED: " + id)
                    return False
                return True

    def _getUrl(self, _uri):
        return (self.fiwareAddress + "/" + self.NGSI_VERSION + "/" + _uri)

    def _getUrlv1(self):
        return (self.fiwareAddress + "/v1/updateContext")       

    def shutDown(self):
        self.unregister_entities()