__author__ = "Peter Detzner" 
__maintainer__ = "Peter Detzner"
__version__ = "0.0.1a"
__status__ = "Developement"

import signal
import sys
import os
from sys import exit
from os import environ
from setup import app
#import app

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
from Entities import task, taskState
from Entities import san
from Entities import ran
from icent import IcentDemo
import servercheck

# from Entities import task.Task
# from Entities import taskstate.TaskState

HOST = '0.0.0.0'
PORT = 5555
SERVER_ADDRESS = "localhost"


CONFIG_FILE = "./fiware_config.ini"
parsedConfigFile = Config(CONFIG_FILE)
ocbHandler = ContextBrokerHandler(parsedConfigFile.getFiwareServerAddress())
icentStateMachine = IcentDemo("Anda")
 
currenTaskDesc = task.Task()
currentTaskState = taskState.TaskState()
ran_task_id = 0  
terminate = False 

import requests
import httplib

def deleteSubscriptionById(id):
    if(len(id)>1):
        try:
            print "Deleting " + id 
            print parsedConfigFile.getFiwareServerAddress()+"/v2/subscriptions/"+ id
            response = requests.request("DELETE", parsedConfigFile.getFiwareServerAddress()+"/v2/subscriptions/"+ id)  
            if(response.status_code // httplib.OK == 1):
                print "Success"
        except expression as Exception:
            print "Failed"
            return False
        return True

def signal_handler(sig, frame):
    print('You pressed Ctrl+C!')
    global terminate
    terminate = True 
    print "cleaning up"

    

def flaskThread():
    app.run(host= parsedConfigFile.FLASK_HOST, port= parsedConfigFile.TASKPLANNER_PORT, threaded=True,use_reloader=False, debug = True)

def convertRanState(jsonReq):
    loaded_r = (jsonReq['status_channel'])
    loaded_r = loaded_r['value']
    loaded_r = loaded_r.replace("%27",'"');
    d = json.loads(loaded_r)
    return d


def ranDealer(q):
    global icentStateMachine
    global ocbHandler
    global currentTaskState
    isMoving = False
    while(True):
        jsonReq, entityType = q.get()
        jsonReq = jsonReq[0]
        print "received RAN" 
        if(entityType == "opil_v1.msg.RANState"):
            # todo: check for state
            d = None
            if("status_channel" in jsonReq):
                d = convertRanState(jsonReq)
                global ran_task_id
                if (d["current_task_id"]["id"] != ran_task_id):
                    print "change"
                    print d["current_task_id"]["id"]
                    print ran_task_id
                ran_task_id = d["current_task_id"]["id"]
            if(d):
                if(d["ran_status"] == 1):
                    isMoving = True
                if(isMoving):
                    # if a position of the AGV has reached do the following:
                        # agv --> setActionMotion(Do nothing) and publish it
                        # update taskState and publish it
                        # change state of stateMachine
                    if(icentStateMachine.state == "ran2LoadingDestination" and d["ran_status"]==0):
                        isMoving = False
                        print "reached destination@Loading"         
                        ocbHandler.update_entity_dirty(getActionChannel(d["current_task_id"]["id"]))
                         
                        currentTaskState.state = taskState.State.Running
                        currentTaskState.userAction = taskState.UserAction.WaitForLoading
                        ocbHandler.update_entity(currentTaskState)

                        # change state
                        icentStateMachine.AgvArrivedAtLoadingDestination()
                        
                    elif(icentStateMachine.state == "ran2UnloadingDestination" and d["ran_status"]==0):
                        isMoving = False
                        print "reached destination@Unloading"            
                        ocbHandler.update_entity_dirty(getActionChannel(d["current_task_id"]["id"]))

                        currentTaskState.state = taskState.State.Running
                        currentTaskState.userAction = taskState.UserAction.WaitForUnloading
                        ocbHandler.update_entity(currentTaskState)

                        icentStateMachine.AgvArrivedAtUnloadingDestination()
                    elif(icentStateMachine.state == "ran2WaitingArea" and d["ran_status"]==0):                    
                        isMoving = False
                        print "reached destination@Waiting"                        
                        ocbHandler.update_entity_dirty(getActionChannel(d["current_task_id"]["id"]))    
                        # perform transistin of state: Running --> Finished
                        currentTaskState.state = taskState.State.Finished
                        currentTaskState.userAction = taskState.UserAction.Idle
                        ocbHandler.update_entity(currentTaskState) 
                        # perform transistin of state: Finished --> Idle
                        currentTaskState.state = taskState.State.Idle
                        currentTaskState.userAction = taskState.UserAction.Idle
                        ocbHandler.update_entity(currentTaskState)
                        icentStateMachine.AgvArrivedAtWaitingArea() 

                    print icentStateMachine.state

def findSanById(_sensorData, _id):
    for sensorArrayItem in _sensorData:

        for sensorData in sensorArrayItem['sensorData']['value']:
             
            if(sensorData['sensorType']['value'] == "IR Sensor" and sensorData['sensorId']['value'] == _id):
                return sensorData['readings']['value']

def isButtonPressed(values):
    for reading in values:
        if(reading['reading']['value'] == True):
            return True
    return False 

def sanDealer(q):
    global icentStateMachine     
    global ocbHandler
    while True: 
        jsonReq, entityType = q.get() 
        #jsonReq = jsonReq[0]
        if(entityType == "SensorAgent"):
            if(icentStateMachine.state == "wait4ran2loading"):
                # to do: check for SAN_ID, Type and Value
                # make sure this is a Switch Sensor and it is the value of 1
                readings = findSanById(jsonReq, "IR_1")
                if(readings):
                    if(isButtonPressed(readings)):
                        currentTaskState.state = taskState.State.Running
                        currentTaskState.userAction = taskState.UserAction.Idle
                        ocbHandler.update_entity(currentTaskState) 

                        retVal = getMotionChannel(parsedConfigFile.unloadingArea)
                        ocbHandler.update_entity_dirty(retVal)                        
                        icentStateMachine.AgvIsLoaded()
                        print retVal
  
                # send agv to unload destination
                # todo: send agv to destinatin
            elif(icentStateMachine.state == "wait4ran2unloading"):
                # to do: check for SAN_ID, Type and Value
                readings = findSanById(jsonReq, "IR_2")
                if(readings):
                    if(isButtonPressed(readings)):
                        currentTaskState.state = taskState.State.Running
                        currentTaskState.userAction = taskState.UserAction.Idle
                        ocbHandler.update_entity(currentTaskState) 
                        retVal = getMotionChannel(parsedConfigFile.waitingArea) # ATTENTION: NEED TO FIX THE LOCATION --> Waiting Area
                        ocbHandler.update_entity_dirty(retVal)
                        print retVal
                        # agv is unloaded manually and confirmed
                        icentStateMachine.AgvIsUnloaded()
                # send AGV to waiting area
            print icentStateMachine.state
        else:
            print "Not a known Entitytype\n"
 
def getActionChannel(task_id):
    j2_env = Environment(loader=FileSystemLoader("./Templates"), trim_blocks=True)
    retVal = j2_env.get_template('action_channel.template').render(robot_id = parsedConfigFile.robot_id, task_id=task_id)
    retVal = retVal.replace('\t', '').replace('\n', '')
    return retVal

def getMotionChannel(area):
    j2_env = Environment(loader=FileSystemLoader("./Templates"), trim_blocks=True)
    new_task_id = ran_task_id
    # if(new_task_id > 1):
    #     new_task_id += 1
    retVal = j2_env.get_template('motion_channel.template').render(area=area, robot_id = parsedConfigFile.robot_id, task_id=new_task_id)
    retVal = retVal.replace('\t', '').replace('\n', '')
    return retVal

def taskDealer(q):    
    global icentStateMachine  
    global currentTaskState
    global ocbHandler
    global currenTaskDesc
    while True: 
        jsonReq, entityType = q.get()
        jsonReq = jsonReq[0]
        if(entityType == "Task"):
            entityTask = task.Task() #taskState.getCurrentTaskId() 
            objectFiwareConverter.ObjectFiwareConverter.fiware2Obj(jsonReq,entityTask,useMetadata=False)
            if(icentStateMachine.state == "idle" and entityTask.taskId == currenTaskDesc.taskId and entityTask.state == task.TaskState.Start):
                if(entityTask.state == task.TaskState.Start):
                    icentStateMachine.NewTask()
                    currentTaskState.taskId = currenTaskDesc.taskId
                    currentTaskState.state = taskState.State.Running
                    currentTaskState.userAction = taskState.UserAction.Idle
                    ocbHandler.update_entity(currentTaskState)
                    # prepare of sending motionassignment tasks
                    retVal = getMotionChannel(parsedConfigFile.loadingArea)
                    ocbHandler.update_entity_dirty(retVal)
                    
                    print icentStateMachine.state  
                    #print render_template('./Templates.motion_channel.template',)
                # todo: Send AGV to LoadingDestination
            elif(icentStateMachine.state == "error" and entityTask.state == task.TaskState.Reset):
                icentStateMachine.Reset()
                currentTaskState.taskId = currenTaskDesc.taskId
                currentTaskState.state = taskState.State.Waiting
                currentTaskState.userAction = taskState.UserAction.Idle
                currentTaskState.errorMessage = "Please restart the task"
                ocbHandler.update_entity(currentTaskState)
                print icentStateMachine.state                        
            elif(entityTask.state== task.TaskState.EmergencyStop):
                # todo: stop the robot
                icentStateMachine.Panic()
                currentTaskState.taskId = currenTaskDesc.taskId
                currentTaskState.state = taskState.State.Aborted
                currentTaskState.userAction = taskState.UserAction.Idle
                currentTaskState.errorMessage = "Please reset the task"
                ocbHandler.update_entity(currentTaskState)
                print icentStateMachine.state

def obj2JsonArray(_obj):
    tempArray = []
    tempArray.append(_obj)
    print json.dumps(tempArray)
    return (tempArray)

if __name__ == '__main__': 
    global subscriptionDict
    global stateQueue 
    global ocbHandler
    global currenTaskDesc
    global currentTaskState

    signal.signal(signal.SIGINT, signal_handler)
    checkIfServerIsUpRunning = threading.Thread(name='checkServerRunning', 
                                                target=servercheck.checkServerRunning, 
                                                args=(SERVER_ADDRESS, parsedConfigFile.TASKPLANNER_PORT,))


    flaskServerThread = threading.Thread(name= 'flaskThread',target = flaskThread) 

    checkIfServerIsUpRunning.start()       
     
    flaskServerThread.start() 
    print "wait for finish"
    checkIfServerIsUpRunning.join()
    # create an instance of the fiware ocb handler
    

# few things commented due to the damn airplane mode 
    # publish first the needed entities before subscribing ot it
    ocbHandler.create_entity(currentTaskState) 
    ocbHandler.create_entity(currenTaskDesc) 

    # subscribe to entities
    subscriptionId = ocbHandler.subscribe2Entity( _description = "notify me",
            _entities = obj2JsonArray(task.Task.getEntity()),  
            _notification = parsedConfigFile.getTaskPlannerAddress() +"/task",)
    globals.subscriptionDict[subscriptionId] ="Task"     

    #globals.subscriptionDict[subscriptionId] = task.Task.Type()
    subscriptionId = ocbHandler.subscribe2Entity( _description = "SAN Updates Notification",
            _entities = obj2JsonArray(san.San.getEntity()),  
            _notification = parsedConfigFile.getTaskPlannerAddress() +"/san",)     
    globals.subscriptionDict[subscriptionId] ="SensorAgent"       
     
      
    subscriptionId = ocbHandler.subscribe2Entity( _description = "subscriber",
            _entities = obj2JsonArray(ran.Ran.getEntity()), _condition_attributes="status_channel",  
            _notification = parsedConfigFile.getTaskPlannerAddress()+"/ran",)
    globals.subscriptionDict[subscriptionId] = "opil_v1.msg.RANState"             


    # this is just for mockup
    #globals.subscriptionDict["0"] = "Task"
    #globals.subscriptionDict["5be488a24c31e6381bfca96b"] = "SensorAgent"
    #globals.subscriptionDict["2"] = "RAN"

    # entityAttributeChangePublisher = EntityAttributeChangeObserver(parsedConfigFile.getFiwareServerAddress())
 
    # taskMon = TaskMonitoring()
     
    # # before registering/publishing the entities, attaching is required
    # ocbHandler.attach_entity(taskMon)
    # # after adding it to the ocbHandler, feel free to register/publish the entities
    # ocbHandler.register_entities();
    
    # taskMon.attach_publisher(entityAttributeChangePublisher);
    
    # taskMon.time = "23";
    # # wait until server is available

    print "Setting up working Threads for Task, RAN, SAN"
    workerTask = Thread(target=taskDealer, args=(globals.taskQueue,))
    workerSan = Thread(target=sanDealer, args=(globals.sanQueue,))
    workerRan = Thread(target=ranDealer, args=(globals.ranQueue,))
    workerTask.start()
    workerSan.start()
    workerRan.start()
    
    print "Done"
    print "Publishing TaskState"
    # currentTaskState.taskId = taskState.getCurrentTaskId()
    # currentTaskState.state = taskState.State.Idle
    # currentTaskState.userAction = taskState.UserAction.Idle
    # ocbHandler.update_entity(currentTaskState)
    print "Done"

    print "Push Ctrl+C to exit()"

    user_input = ""
    while terminate == False:
        pass

    for item in globals.subscriptionDict:
        deleteSubscriptionById(item)
        

    # todo: delete subscriptions
    # ocbHandler.unregister_entities()
    # #SubscribtionHandler.unsubscribeContext(parsedConfigFile)
    print "shutdown flask"    
    os._exit(0)