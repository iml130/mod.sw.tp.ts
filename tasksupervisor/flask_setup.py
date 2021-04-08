import os
import logging
import http.client
import json
import jsonschema

from flask import Flask
from flask import Blueprint
from flask import request
from flask import send_file

# import my_globals
from tasksupervisor import my_globals

FI_SUB_ID = "subscriptionId"
FI_DATA = "data"

VERSION = """Fraunhofer IML<br />
TaskPlanner v3.4.6 - 15.10.2020 (#06041986)<br />
Running...<br />
"""

logger = logging.getLogger(__name__)
materialflow_schema = open("./tasksupervisor/endpoints/materialflow_schema.json").read()

def create_flask_app(interface):
    app = Flask(__name__)
    logger.info("Registering Blueprints")
    app.register_blueprint(construct_blueprint_sensor(interface), url_prefix='/san')
    app.register_blueprint(construct_blueprint_materialflow(interface), url_prefix='/materialflow')

    logger.info("Registering Blueprints_done")

    @app.route('/')
    @app.route('/home')
    def home():
        """Renders the landing page where a version number is returned."""
        return (VERSION, http.client.OK)

    return app

def construct_blueprint_sensor(interface):
    sensor_agent_node_blueprint = Blueprint(
        'sensor_agent_node_endpoint', __name__)

    @sensor_agent_node_blueprint.route('/<token>', methods=['GET', 'POST'])
    def sensor_agent_node_endpoint(token):
        """ Endpoint for the Sensor Agent to handle update notification """
        if request.json:
            json_request = request.json
            #dictQueue.put_data(token, jsonReq)
            if FI_SUB_ID in json_request and FI_DATA in json_request:
                interface.retreive(json_request)
            else:
                # no subscription
                logger.info("sanEndpoint: No Subscription in List")
        else:
            logger.info("sanEndpoint: No json in request")
        return "ok", http.client.OK

    return sensor_agent_node_blueprint

def construct_blueprint_materialflow(interface):

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
                jsonschema.validate(
                    json_requests['data'][0], json.loads(materialflow_schema))
            except jsonschema.ValidationError as err:
                logger.error(
                    "Materialflow Endpoint ValidationError: %s", str(err.message))
                return err.message, http.client.BAD_REQUEST
            except jsonschema.SchemaError as err:
                logger.error(
                    "Materialflow Endpoint SchemaError: %s", str(err.message))
                return err.message, http.client.INTERNAL_SERVER_ERROR
            except:
                logger.error("General error")

            if(FI_SUB_ID in json_requests and FI_DATA in json_requests):
                subscription_id = json_requests[FI_SUB_ID]
                # a lock is needed ohterwise it is possible that we receive a notification BEFORE we could add it
                # if this doesnt work, a work around could be a delay of handling the notification (time.sleep(0.5))
                with my_globals.lock:
                    interface.retreive(json_requests)
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