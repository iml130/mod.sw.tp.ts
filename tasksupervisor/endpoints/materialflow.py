import os
import logging
import http.client
import json
import jsonschema

# third party imports
from flask import Blueprint
from flask import request 
from flask import send_file

# import my_globals
from tasksupervisor import my_globals



# local imports
logger = logging.getLogger(__name__)

materialflow_schema = open("./tasksupervisor/endpoints/materialflow_schema.json").read()

def construct_blueprint_materialflow(task_supervisor):

    materialflow_blueprint = Blueprint('materialflow_endpoint', __name__)

    @materialflow_blueprint.route('', methods=['GET', 'POST'])
    def materialflow_endpoint():
        """ Endpoint for getting a new materialflow description and validates it against a json schema """
        logger.info("taskEP is running and received new data")
        if request.json:
            # handle POST request
            json_requests = request.json
            # decodedString = jsonReq['data'][0]["TaskSpec"]["value"]
            # decodedString = urllib.unquote_plus(decodedString)

            # retVal = checkTaskLanguage(decodedString)

            try:
                jsonschema.validate(json_requests['data'][0], json.loads(materialflow_schema))
            except jsonschema.ValidationError as err:
                logger.error("Materialflow Endpoint ValidationError: %s", str(err.message))
                return err.message, http.client.BAD_REQUEST
            except jsonschema.SchemaError as err:
                logger.error("Materialflow Endpoint SchemaError: %s", str(err.message))
                return err.message, http.client.INTERNAL_SERVER_ERROR
            except:
                logger.error("General error")

            if(my_globals.FI_SUB_ID in json_requests and my_globals.FI_DATA in json_requests):
                subscription_id = json_requests[my_globals.FI_SUB_ID]
                # a lock is needed ohterwise it is possible that we receive a notification BEFORE we could add it
                # if this doesnt work, a work around could be a delay of handling the notification (time.sleep(0.5))
                with my_globals.lock:
                    if subscription_id in task_supervisor.subscription_dict:
                        my_globals.taskQueue.put(
                            (json_requests[my_globals.FI_DATA], task_supervisor.subscription_dict[subscription_id]))
                    else:
                        print("empty something")
                # my_globals.lock.release()

            else:
                # no subscription
                logger.info("taskEndpoint: No Subscription in List")
        else:
            # handle GET request

            if os.path.isfile('../images/task.png'):
                full_filename = "../images/task.png"
            else:
                full_filename = '../images/idle.png'
            return send_file(full_filename, mimetype='image/png')
        return "ok", http.client.CREATED

    return materialflow_blueprint