import logging
import http.client

from flask import Blueprint
from flask import request

# local imports
# import my_globals
from tasksupervisor import my_globals

logger = logging.getLogger(__name__)


# dictQueue = my_globals.sanDictQueue

def construct_blueprint_sensor(task_supervisor, interface):
    sensor_agent_node_blueprint = Blueprint(
        'sensor_agent_node_endpoint', __name__)

    @sensor_agent_node_blueprint.route('/<token>', methods=['GET', 'POST'])
    def sensor_agent_node_endpoint(token):
        """ Endpoint for the Sensor Agent to handle update notification """
        if request.json:
            json_request = request.json
            #dictQueue.put_data(token, jsonReq)
            if my_globals.FI_SUB_ID in json_request and my_globals.FI_DATA in json_request:
                interface.retreive(json_request)
                # subscription_id = json_request[my_globals.FI_SUB_ID]

                # if subscription_id in task_supervisor.subscription_dict:

                #     task_supervisor.sensor_dispatcher.put_data(
                #         task_supervisor.subscription_dict[subscription_id], json_request)
 
            else:
                # no subscription
                logger.info("sanEndpoint: No Subscription in List")
        else:
            logger.info("sanEndpoint: No json in request")
        return "ok", http.client.OK

    return sensor_agent_node_blueprint
