import requests
import json 
import httplib

HEADERS = {"Content-Type" : "application/json"}

def isResponseOk(statusCode):
    if(statusCode >= httplib.OK and statusCode <= httplib.IM_USED): # everything is fine
        return True;
    return False;



class ContextBrokerHandler:

    def __init__(self, fiwareAddress):
        self.fiwareAddress = fiwareAddress
         
        self.published_entities = []
        self.entities = [];

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

        response = requests.post(self.fiwareAddress + "/v2/entities", data=asJson, headers=HEADERS)
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
 
    def subscribe2Entity(self, _entity_id, _endpoint):
        msg =   {  
            "description" : "Notify me",
           "subject": {
                "entities": [{"idPattern": ".*", "type": "" +_entity_id + ""}] 
            },
            "notification": {
                "http": { "url": "http://10.64.10.152:5555/Task" } 
            }
        }   
        print msg 
        try:
            response = requests.post(self.fiwareAddress + "/v2/subscriptions", data=json.dumps(msg), headers=HEADERS, timeout = 0.5)
            print response.headers.get('Location')

        except requests.exceptions.Timeout:
            pass
        
        return "57458eb60962ef754e7c0998", "Task"
        
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
