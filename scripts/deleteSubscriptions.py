__author__ = "ptrdtznr"
__status__ = "Dev"

# gobal imports

import requests
import httplib


# local imports
import ocb

def deleteSubscriptionById(id):
    try:
        print "Deleting " + id 
        response = requests.request("DELETE", ocb.getAddress(ocb.SUBSCRIPTIONS)+ id)  
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
            


def deleteAllSubscriptions():
    response = requests.request("GET", ocb.getAddress(ocb.SUBSCRIPTIONS))  
    if(response.status_code // httplib.OK == 1):
        for subscription in response.json():
            deleteSubscriptionById(subscription['id'])
        
deleteAllSubscriptions()
#deleteSubscriptionByEntityType("Type")