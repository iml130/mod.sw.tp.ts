__author__ = "ptrdtznr"
__status__ = "Dev"

# gobal imports

import requests
import httplib


# local imports
import ocb
import sys
def deleteEntitiesById(id):
    try:
        print "Deleting " + id 
        response = requests.request("DELETE", ocb.getAddress(ocb.ENTITIES)+ id)  
        if(response.status_code // httplib.OK == 1):
            print "Success"
    except expression as Exception:
        print "Failed"
        return False
    return True

def deleteSubscriptionByEntityType(entityType):
    response = requests.request("GET", ocb.getAddress(ocb.SUBSCRIPTIONS))  
    if(response.status_code // httplib.OK == 1):
        for subscription in response.json():
            for entity in subscription["subject"]["entities"]:
                if(entity["type"] == entityType):
                    deleteSubscriptionById(subscription['id'])
            


def deleteAllEntitiesByType(entityType):
    response = requests.request("GET", ocb.getAddress(ocb.ENTITIES))  
    if(response.status_code // httplib.OK == 1):
        for subscription in response.json(): 
            if(subscription['type'] == entityType):
                deleteEntitiesById(subscription['id'])
                
if len(sys.argv) != 2:
    print("invalid number of arguments, please provide the file name of entities")
    
entityType = sys.argv[1]
print entityType
deleteAllEntitiesByType(entityType)
#deleteSubscriptionByEntityType("Type")