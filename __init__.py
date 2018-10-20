"""
The flask application package.
"""

from flask import Flask


app = Flask(__name__)

import views
  

print "register blueprints"
# app.register_blueprint(mod_sw_taskplanner, url_prefix='/mod.sw.tp')
# app.register_blueprint(mod_test , url_prefix='/test')
print "register done"