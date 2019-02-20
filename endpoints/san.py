from flask import Blueprint
from flask import request 
from threading import Event, Thread

import json

#local imports 
import globals

san_bp = Blueprint('sanEndpoint', __name__)

dictQueue = globals.sanDictQueue

@san_bp.route('/<token>', methods=['GET', 'POST']) 
def sanEndPoint(token):
    """Renders the home page.""" 
    if request.json:  
        dictQueue.putData(token, "funzt")
        jsonReq = request.json
        if(globals.FI_SUB_ID in jsonReq and globals.FI_DATA in jsonReq):
            subId =jsonReq[globals.FI_SUB_ID] 
            if(subId in globals.subscriptionDict): 
                globals.sanQueue.put( (jsonReq[globals.FI_DATA], globals.subscriptionDict[subId]) )
        else:
            # no subscription 
            print "narf"
    else:
        print "no json"
    return "ok", 201
     