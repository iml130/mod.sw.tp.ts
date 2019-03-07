"""
Routes and views for the flask application.
"""
import json
from flask import request 
from threading import Event, Thread
from datetime import datetime
from flask import render_template,Response
from setup import app
from Queue import Queue

import httplib
#from version import Version 
import globals
from setup import VERSION

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return (VERSION,httplib.OK)

