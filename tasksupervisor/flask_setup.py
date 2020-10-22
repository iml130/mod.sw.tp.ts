import logging
import http.client

from flask import Flask

from tasksupervisor.endpoints.sensor_agent_node import construct_blueprint_sensor
from tasksupervisor.endpoints.materialflow import construct_blueprint_materialflow


VERSION = """Fraunhofer IML<br />
TaskPlanner v3.4.6 - 15.10.2020 (#06041986)<br />
Running...<br />
"""

logger = logging.getLogger(__name__)


def create_flask_app(tasksupervisor_knowledge):
    app = Flask(__name__)
    logger.info("Registering Blueprints")
    app.register_blueprint(construct_blueprint_sensor(
        tasksupervisor_knowledge), url_prefix='/san')
    app.register_blueprint(construct_blueprint_materialflow(
        tasksupervisor_knowledge), url_prefix='/materialflow')
    #app.register_blueprint(mod_test , url_prefix='/test')
    logger.info("Registering Blueprints_done")

    @app.route('/')
    @app.route('/home')
    def home():
        """Renders the landing page where a version number is returned."""
        return (VERSION, http.client.OK)

    return app
