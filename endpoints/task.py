from flask import Blueprint
from flask import request 
from threading import Event, Thread

import json

#local imports 
import globals


task_bp = Blueprint('taskEndpoint', __name__)

@task_bp.route('', methods=['GET', 'POST']) 
def task():
    """Renders the home page.""" 
    if request.json:
        print request.json
        jsonReq = request.json
        if(globals.FI_SUB_ID in jsonReq and globals.FI_DATA in jsonReq):
            subId =jsonReq[globals.FI_SUB_ID] 
            if(subId in globals.subscriptionDict): 
                globals.taskQueue.put((jsonReq[globals.FI_DATA], globals.subscriptionDict[subId]) )
        else:
            # no subscription   
            print "narf"
    else:
        print "no json"
    return "ok", 201
 