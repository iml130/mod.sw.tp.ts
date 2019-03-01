from flask import Blueprint
from flask import request 
from threading import Event, Thread
import httplib
import json
import jsonschema
import urllib
#local imports 
import globals
from flask import render_template, request, url_for
from flask import send_file 
import os 
task_bp = Blueprint('taskEndpoint', __name__)

 
import logging

logger = logging.getLogger(__name__)

schema = open("./endpoints/taskSchema.json").read()

@task_bp.route('', methods=['GET', 'POST']) 
def task():
    logger.info("taskEP is running")
    """Renders the home page.""" 
    if request.json: 
        jsonReq = request.json
        # decodedString = jsonReq['data'][0]["TaskSpec"]["value"]
        # decodedString = urllib.unquote_plus(decodedString)
        
        # retVal = checkTaskLanguage(decodedString) 
        
        # check if the TaskLanguage is VALID
        # if valid? --> Parse
        # do the rest
            # subscribe to events
            # start a task when an event has been triggered

        # jsonschema.validate(jsonReq, schema)
        # try:
        #     jsonschema.validate(jsonReq['data'][0], json.loads(schema))
        # except jsonschema.ValidationError as e:
        #     return httplib.BAD_REQUEST, e.message
        # except jsonschema.SchemaError as e:
        #     return httplib.INTERNAL_SERVER_ERROR, e.message
            
        if(globals.FI_SUB_ID in jsonReq and globals.FI_DATA in jsonReq):
            subId =jsonReq[globals.FI_SUB_ID] 
            if(subId in globals.subscriptionDict): 
                globals.taskQueue.put((jsonReq[globals.FI_DATA], globals.subscriptionDict[subId]))
        else:
            # no subscription  
            logger.info("taskEndpoint: No Subscription in List")
    else:
        if(os.path.isfile('./images/task.png')):
            full_filename = "./images/task.png"
        else:
            full_filename = './images/idle.png'
        return send_file(full_filename, mimetype='image/png')
    return "ok", httplib.CREATED
 