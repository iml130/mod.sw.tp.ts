import logging
from flask import Flask

app = Flask(__name__)

VERSION = """Fraunhofer IML<br />
OPIL TaskPlanner v0.0.1 - 07.03.2018<br />
Running...<br />
"""
import views 

from endpoints.san import san_bp
from endpoints.task import task_bp
from endpoints.ran import ran_bp

logger = logging.getLogger(__name__)

logger.info("Registering Blueprints")

app.register_blueprint(san_bp, url_prefix='/san')
app.register_blueprint(task_bp, url_prefix='/task')
app.register_blueprint(ran_bp, url_prefix='/ran')
#app.register_blueprint(mod_test , url_prefix='/test')
logger.info("Registering Blueprints_done")