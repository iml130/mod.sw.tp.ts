__author__ = "ptrdtznr"
__status__ = "Dev"

# gobal imports

import requests
import httplib
import json

# local imports
import ocb
HEADER = {"Content-Type" : "application/json"}

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
            


def subscription_update(subscription_id, status=None, subject= None, notification = None, description=None,
        entities=None, condition_attributes=None, condition_expression=None,
        notification_attrs=None, notification_attrs_blacklist=None,
        http=None, http_custom=None,
        attrs_format=None, metadata=None,
        expires=None, throttling=None):

        subscription = {}
        if status:
            subscription["status"] = status
 
        # if description:
        #     subscription["description"] = description
        # # General
        if expires:
            subscription["expires"] = expires
        # if throttling:
        #     subscription["throttling"] = throttling

        # # subject
        # condition = {}
        # if condition_attributes:
        #     condition["attrs"] = condition_attributes
        # if condition_expression:
        #     condition["expression"] = condition_expression

        # subject = {}
        # if entities:
        #     subject["entities"] = entities
        # if condition:
        #     subject["condition"] = condition

        if subject:
            subscription["subject"] = subject

        # Notification
        if(notification):
            subscription["notification"] = notification

        # if notification_attrs:
        #     notification["attrs"] = notification_attrs
        # if notification_attrs_blacklist:
        #     notification["exceptAttrs"] = notification_attrs_blacklist

        # Check if one and only one is defined
        # if http:
        #     notification["http"] = {"url": http}

        # if http_custom:
        #     notification["httpCustom"] = http_custom

        # if attrs_format:
        #     notification["attrsFormat"] = attrs_format
        # if metadata:
        #     notification["metadata"] = metadata

        # if notification:
        #     subscription["notification"] = notification
        print json.dumps(subscription)
        print "address: " + ocb.getAddress(ocb.SUBSCRIPTIONS) + subscription_id

        response = requests.request("PATCH", ocb.getAddress(ocb.SUBSCRIPTIONS) + subscription_id,
            json=subscription, headers=HEADER)
        print response.status_code, response.text

def deleteAllSubscriptions():
    response = requests.request("GET", ocb.getAddress(ocb.SUBSCRIPTIONS))  
    response =  response.content.replace("172.17.0.1", "10.64.10.152")
    t=json.loads(response)
    for item in t:
        subscription_update(subscription_id = item['id'], subject = item['subject'], notification = item['notification'], expires= item['expires'])       
 
    #if(response.status_code // httplib.OK == 1):
    #    for subscription in response.json():
    #        deleteSubscriptionById(subscription['id'])
        
deleteAllSubscriptions()
#deleteSubscriptionByEntityType("Type")