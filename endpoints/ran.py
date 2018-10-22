from flask import Blueprint
from flask import request 
from threading import Event, Thread

import json

#local imports 
import globals

ran_bp = Blueprint('ranEndpoint', __name__)



@ran_bp.route('', methods=['GET', 'POST']) 
def ranEndPoint():
    """Renders the home page.""" 
    if request.json: 
        jsonReq = request.json
        if(globals.FI_SUB_ID in jsonReq and globals.FI_DATA in jsonReq):
            subId =jsonReq[globals.FI_SUB_ID] 
            if(subId in globals.subscriptionDict): 
                globals.ranQueue.put( (jsonReq[globals.FI_DATA], globals.subscriptionDict[subId]) )
        else:
            # no subscription 
            print "narf"
    else:
        print "no json"
    return "ok", 201
     