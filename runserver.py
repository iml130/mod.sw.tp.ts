"""
This script runs the Template application using a development server.
"""

from os import environ
# from . import app
from __init__ import app
import time
import urllib2
import threading
from threading import Event, Thread
from flask import g 
from flask import render_template,Response
from Queue import Queue
import json
from datetime import datetime

# local imports
import globals 
from configParser import Config
from contextbrokerhandler import ContextBrokerHandler
from FiwareObjectConverter import objectFiwareConverter
from Entities import task

HOST = '0.0.0.0'
PORT = 5555
SERVER_ADDRESS = "localhost"

CONFIG_FILE = "./fiware_config.ini"
parsedConfigFile = Config(CONFIG_FILE)
  
def flaskThread():
    app.run(host= '0.0.0.0', port= PORT, threaded=True,use_reloader=False, debug = True)
    
def checkServerRunning():
    doForever = True    
    while doForever:
        print "checkServerRunning"
         
        try:
            request = urllib2.Request("http://"+ SERVER_ADDRESS+  ":" + str(PORT) ) 
            response = urllib2.urlopen(request)        
            doForever = False
        except urllib2.HTTPError, err:
            print('HTTPError = ' + str(err.code))
        except urllib2.URLError, err:
            print('URLError = ' + str(err.reason))
        except httplib.HTTPException, err:
            print('HTTPException')
        else:
            print "FAILED"
    print "Thread is ending"


def do_stuff(q):
    while True:
        jsonReq = json.dumps(q.get()[0]) 
        # tt = task.Task()
        # print jsonReq
        # tt = objectFiwareConverter.ObjectFiwareConverter.fiware2Obj(jsonReq,tt,useMetadata=False)
        # print jsonReq
        print "und weiter geht\n"


if __name__ == '__main__': 
    global subscriptionDict
    global stateQueue 
    
    checkIfServerIsUpRunning = threading.Thread(name='checkServerRunning', 
                                                target=checkServerRunning)

    flaskServerThread = threading.Thread(name= 'flaskThread',target = flaskThread) 

    checkIfServerIsUpRunning.start()       
     
    flaskServerThread.start() 
    print "wait for finish"
    checkIfServerIsUpRunning.join();
    # # create an instance of the fiware ocb handler
    ocbHandler = ContextBrokerHandler(parsedConfigFile.getFiwareServerAddress())
    id, Task = ocbHandler.subscribe2Entity("Task", "/Task")
    globals.subscriptionDict[id] = Task
    # entityAttributeChangePublisher = EntityAttributeChangeObserver(parsedConfigFile.getFiwareServerAddress())

    # taskMon = TaskMonitoring()
     
    # # before registering/publishing the entities, attaching is required
    # ocbHandler.attach_entity(taskMon)
    # # after adding it to the ocbHandler, feel free to register/publish the entities
    # ocbHandler.register_entities();
    
    # taskMon.attach_publisher(entityAttributeChangePublisher);
    
    # taskMon.time = "23";
    # # wait until server is available
    worker = Thread(target=do_stuff, args=(globals.stateQueue,))
    worker.daemon = True
    worker.start()

    
    print "Done"
    user_input = ""
    while user_input!= "exit":
        user_input = raw_input("-->")
            
    # ocbHandler.unregister_entities()
    # #SubscribtionHandler.unsubscribeContext(parsedConfigFile)
    # print "shutdown flask"    

