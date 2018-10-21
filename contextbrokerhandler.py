import requests
import json 
import httplib



def isResponseOk(statusCode):
    if(statusCode >= httplib.OK and statusCode <= httplib.IM_USED): # everything is fine
        return True
    return False


ENTITIES = "entities"
SUBSCRIPTIONS = "subscriptions"

    
class ContextBrokerHandler:
    HEADER = {"Content-Type" : "application/json"}
    HEADER_NO_PAYLOAD = {
        "Accept": "application/json"
    }

    TIMEOUT = 0.5
    NGSI_VERSION = "v2"

    def __init__(self, fiwareAddress):
        self.fiwareAddress = fiwareAddress
        self.fiwareAddress = "Http://localhost:1026"
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
        if(self.delete_entity(entityInstance)):
            print "error"

        entity = Entity()
        entity.convertObjectToEntity(entityInstance) 
        asJson = JsonConvert.ToJSON(entity)
        print asJson

        response = requests.post(self._getUrl(ENTITIES) , data=asJson, headers=HEADERS)
        statusCode = response.status_code;
        if(isResponseOk(statusCode)): # everything is fine
            self.published_entities.append(entityInstance)
            print "Status OK"
        elif(statusCode == httplib.BAD_REQUEST): # everything is NOT fine
            print "httplib.UNPROCESSABLE_ENTITY"
            content = json.loads(response.content)
            print content
        else:
            print statusCode
            print response

        # update of an entity:
        #elif(statusCode == httplib.UNPROCESSABLE_ENTITY): # everything is fine
        #    print "httplib.UNPROCESSABLE_ENTITY"
        #    response = requests.patch(self.fiwareAddress + "/v2/entities/" + str(entity.id) + "/attrs", data=asJson, headers=HEADERS)
        #    statusCode = response.status_code;
        #    print statusCode

    def delete_entity(self, entityInstance):
        print "Delete Entity - Id: " + str (entityInstance)
        entity = Entity()
        entity.convertObjectToEntity(entityInstance) 
        response = requests.delete(self.fiwareAddress + "/v2/entities/" + str(entity.id))
        statusCode = response.status_code;
        
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

    def update_entity(self, msg):
        self.msg_queue.append(msg)

    def subscribe(self, msg, subscriber):
        self.subscribers.setdefault(msg, []).append(subscriber)

    def unsubscribe(self, msg, subscriber):
        self.subscribers[msg].remove(subscriber)

    def update(self):
        for msg in self.msg_queue:
            for sub in self.subscribers.get(msg, []):
                sub.run(msg)
        self.msg_queue = []
 
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
            condition["attrs"] = condition_attributes
        if _condition_expression:
            condition["expression"] = condition_expression

        subject = {}
        subject["entities"] = _entities
        if(condition):
            subject = {"condition": condition}
        
        msg["subject"] = subject

        notification = {}
        if _notification:
            notification["http"] = { "url" : _notification}

        msg["notification"] = notification
        if _expires:
            subscription["expires"] = _expires
        if _throttling:
            subscription["throttling"] = _throttling

        # msg =   {  
        #     "description" : "Notify me",
        #    "subject": {
        #         "entities": [{"idPattern": ".*", "type": "" +_entityType + ""}] 
        #     },
        #     "notification": {
        #         "http": { "url": "" } 
        #     }
        # }   
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
            
        elif(statusCode == httplib.BAD_REQUEST): # everything is NOT fine
            print "httplib.UNPROCESSABLE_ENTITY"
            content = json.loads(response.content)
            print content
        else:
            print statusCode
            print response
        
        return response.headers.get('Location')
    def _getUrl(self, _uri):
        return (self.fiwareAddress + "/" + self.NGSI_VERSION + "/" + _uri)
       