__author__ = "Peter Detzner" 
__maintainer__ = "Peter Detzner"
__version__ = "0.0.1a"
__status__ = "Developement"


import logging
from flask import Flask

app = Flask(__name__)

VERSION = """Fraunhofer IML<br />
TaskPlanner v3.1.6 - 13.07.2020 (#06041986)<br />
Running...<br />
"""
import views 

from Endpoints.san import san_bp
from Endpoints.task import task_bp
 

logger = logging.getLogger(__name__)

logger.info("Registering Blueprints")

app.register_blueprint(san_bp, url_prefix='/san')
app.register_blueprint(task_bp, url_prefix='/task') 
#app.register_blueprint(mod_test , url_prefix='/test')
logger.info("Registering Blueprints_done")