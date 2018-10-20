"""
Routes and views for the flask application.
"""
import json
from flask import request

from datetime import datetime
from flask import render_template,Response
from __init__ import app
from Queue import Queue
#from version import Version 
import globals
from statemachine import StateMachine

subscriptionId = "subscriptionId"
data = "data"

@app.route('/')
@app.route('/home')
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Home Page',
        year=datetime.now().year,
    )
 
@app.route('/Task', methods=['GET', 'POST']) 
def task():
    """Renders the home page."""
    print "test"
    if request.json:
        print request.json
        jsonReq = request.json
        if('subscriptionId' in jsonReq and 'data' in jsonReq):
            print "continue"
            print jsonReq[subscriptionId] 
            if(jsonReq[subscriptionId] in globals.subscriptionDict):
                #subscriptions.append(jsonReq[subscriptionId])
                globals.stateQueue.put(jsonReq[data])
                
        else:
            print "narf"
    else:
        print "no json"
    return "ok", 201
 