"""
The flask application package.
"""

from flask import Flask


app = Flask(__name__)

import views 

from endpoints.san import san_bp
from endpoints.task import task_bp
from endpoints.ran import ran_bp


print "register blueprints"
app.register_blueprint(san_bp, url_prefix='/san')
app.register_blueprint(task_bp, url_prefix='/task')
app.register_blueprint(ran_bp, url_prefix='/ran')
#app.register_blueprint(mod_test , url_prefix='/test')
print "register done"