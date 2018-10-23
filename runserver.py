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
from jinja2 import Environment, FileSystemLoader

# local imports
import globals 
from configParser import Config
from contextbrokerhandler import ContextBrokerHandler
from FiwareObjectConverter import objectFiwareConverter
from Entities import task, taskstate
from icent import IcentDemo
import servercheck


HOST = '0.0.0.0'
PORT = 5555
SERVER_ADDRESS = "localhost"

CONFIG_FILE = "./fiware_config.ini"
parsedConfigFile = Config(CONFIG_FILE)
icentStateMachine = IcentDemo("Anda")

currenTaskDesc = task.Task()
currentTaskState = taskstate.TaskState()
  
def flaskThread():
    app.run(host= parsedConfigFile.TASKPLANNER_HOST, port= parsedConfigFile.TASKPLANNER_PORT, threaded=True,use_reloader=False, debug = True)
    

def ranDealer(q):
    global icentStateMachine
    while(True):
        jsonReq, entityType = q.get()
        jsonReq = jsonReq[0]
        print "received RAN"
        if(entityType == "RAN"):
            # todo: check for state
            if(icentStateMachine.state == "ran2LoadingDestination"):
                icentStateMachine.AgvArrivedAtLoadingDestination()
            elif(icentStateMachine.state == "ran2UnloadingDestination"):
                icentStateMachine.AgvArrivedAtUnloadingDestination()
            elif(icentStateMachine.state == "ran2WaitingArea"):
                icentStateMachine.AgvArrivedAtWaitingArea()            
            print icentStateMachine.state

def sanDealer(q):
    global icentStateMachine 
    while True: 
        jsonReq, entityType = q.get() 
        #jsonReq = jsonReq[0]
        if(entityType == "SAN"):
            if(icentStateMachine.state == "wait4ran2loading"):
                # to do: check for SAN_ID, Type and Value

                # AGV is loaded manually and confirmed
                icentStateMachine.AgvIsLoaded()
                # send agv to unload destination
                # todo: send agv to destinatin
            elif(icentStateMachine.state == "wait4ran2unloading"):
                # to do: check for SAN_ID, Type and Value
                
                # agv is unloaded manually and confirmed
                icentStateMachine.AgvIsUnloaded()
                # send AGV to waiting area
            print icentStateMachine.state
        else:
            print "Not a known Entitytype\n"

def taskDealer(q):    
    global icentStateMachine 
    global currentTaskState
    while True: 
        jsonReq, entityType = q.get()
        jsonReq = jsonReq[0]
        if(entityType == "Task"):
            entityTask = task.Task()
            objectFiwareConverter.ObjectFiwareConverter.fiware2Obj(jsonReq,entityTask,useMetadata=False)
            if(icentStateMachine.state == "idle"):
                if(entityTask.taskOrder == task.TaskOrder.New):
                    icentStateMachine.NewTask()
                    currentTaskState.taskId = taskstate.getNewTaskId()
                    ocbHandler.update_entity(currentTaskState);
                    # prepare of sending motionassignment tasks
                    print icentStateMachine.state 
                    j2_env = Environment(loader=FileSystemLoader("./Templates"), trim_blocks=True)
                    print j2_env.get_template('motion_channel.template').render( my_string="Wheeeee!")
                    #print render_template('./Templates.motion_channel.template',)
                # todo: Send AGV to LoadingDestination
            elif(entityTask.taskOrder== task.TaskOrder.EmergencyStop):
                icentStateMachine.Panic()
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
    # create an instance of the fiware ocb handler
    ocbHandler = ContextBrokerHandler(parsedConfigFile.getFiwareServerAddress())

    # publish first the needed entities before subscribing ot it
    ocbHandler.create_entity(currentTaskState) 
    ocbHandler.create_entity(currenTaskDesc) 

    # subscribe to entities
    subscriptionId = ocbHandler.subscribe2Entity( _description = "notify me",
            _entities = obj2JsonArray(task.Task.getEntity()),  
            _notification = "http://localhost:5555/task",)

    globals.subscriptionDict[subscriptionId] = task.Task.Type()

    # this is just for mockup
    globals.subscriptionDict["0"] = "Task"
    globals.subscriptionDict["1"] = "SAN"
    globals.subscriptionDict["2"] = "RAN"

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
    workerRan = Thread(target=ranDealer, args=(globals.ranQueue,))
    workerTask.start()
    workerSan.start()
    workerRan.start()
    
    print "Done"
    user_input = ""
    while user_input!= "exit":
        user_input = raw_input("-->").strip()
            
    # todo: delete subscriptions
    # ocbHandler.unregister_entities()
    # #SubscribtionHandler.unsubscribeContext(parsedConfigFile)
    print "shutdown flask"    

