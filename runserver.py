__author__ = "Peter Detzner" 
__maintainer__ = "Peter Detzner"
__version__ = "0.0.1a"
__status__ = "Developement"

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
from icent import IcentDemo
import servercheck


HOST = '0.0.0.0'
PORT = 5555
SERVER_ADDRESS = "localhost"

CONFIG_FILE = "./fiware_config.ini"
parsedConfigFile = Config(CONFIG_FILE)
icentStateMachine = IcentDemo("Anda")
  
def flaskThread():
    app.run(host= '0.0.0.0', port= PORT, threaded=True,use_reloader=False, debug = True)
    

def sanDealer(q):
    global icentStateMachine 
    while True:
        print threading.current_thread()
        jsonReq, entityType = q.get() 
        #jsonReq = jsonReq[0]
        if(entityType == "SAN"):
            print "received an SAN update"
        else:
            print "Not a known Entitytype\n"

def taskDealer(q):    
    global icentStateMachine 
    while True:
        print threading.current_thread()
        jsonReq, entityType = q.get()
        jsonReq = jsonReq[0]
        if(entityType == "Task"):
            entityTask = task.Task()
            objectFiwareConverter.ObjectFiwareConverter.fiware2Obj(jsonReq,entityTask,useMetadata=False)
            
            if(entityTask.taskOrder == task.TaskOrder.New):
                icentStateMachine.start()
                print icentStateMachine.state
            elif(entityTask.taskOrder== task.TaskOrder.EmergencyStop):
                icentStateMachine.panic()
                print icentStateMachine.state
                
        elif (entityType == "SAN"):
            print "received an SAN update"
        else:
            print "Not a known Entitytype\n"



def obj2JsonArray(_obj):
    tempArray = []
    tempArray.append(_obj)
    print json.dumps(tempArray)
    return (tempArray)

if __name__ == '__main__': 
    global subscriptionDict
    global stateQueue 
    
    checkIfServerIsUpRunning = threading.Thread(name='checkServerRunning', 
                                                target=servercheck.checkServerRunning, 
                                                args=(SERVER_ADDRESS, PORT,))

    flaskServerThread = threading.Thread(name= 'flaskThread',target = flaskThread) 

    checkIfServerIsUpRunning.start()       
     
    flaskServerThread.start() 
    print "wait for finish"
    checkIfServerIsUpRunning.join()
    # # create an instance of the fiware ocb handler
    ocbHandler = ContextBrokerHandler(parsedConfigFile.getFiwareServerAddress())
    print ocbHandler.getEntities()
    subscriptionId = ocbHandler.subscribe2Entity( _description = "notify me",
            _entities = obj2JsonArray({ "id" : "Task1", "type" : "Task"}),  
            _notification = "http://localhost:5555/task",)

    globals.subscriptionDict[subscriptionId] = task.Task.getType()
    globals.subscriptionDict["57458eb60962ef754e7c0999"] = "SAN"

    # entityAttributeChangePublisher = EntityAttributeChangeObserver(parsedConfigFile.getFiwareServerAddress())
 
    # taskMon = TaskMonitoring()
     
    # # before registering/publishing the entities, attaching is required
    # ocbHandler.attach_entity(taskMon)
    # # after adding it to the ocbHandler, feel free to register/publish the entities
    # ocbHandler.register_entities();
    
    # taskMon.attach_publisher(entityAttributeChangePublisher);
    
    # taskMon.time = "23";
    # # wait until server is available
    workerTask = Thread(target=taskDealer, args=(globals.taskQueue,))
    workerSan = Thread(target=sanDealer, args=(globals.sanQueue,))
    workerTask.start()
    workerSan.start()
    
    print "Done"
    user_input = ""
    while user_input!= "exit":
        user_input = raw_input("-->").strip()
            
    # ocbHandler.unregister_entities()
    # #SubscribtionHandler.unsubscribeContext(parsedConfigFile)
    print "shutdown flask"    

