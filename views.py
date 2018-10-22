"""
Routes and views for the flask application.
"""
import json
from flask import request 
from threading import Event, Thread
from datetime import datetime
from flask import render_template,Response
from __init__ import app
from Queue import Queue

import httplib
#from version import Version 
import globals

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return ("OK",httplib.OK)

