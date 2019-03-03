__author__ = "Peter Detzner" 
__maintainer__ = "Peter Detzner"
__version__ = "0.0.1a"
__status__ = "Developement"

import signal
import sys
import os
import urllib
from sys import exit
from os import environ
from setup import app
import logging
import logging.config
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
from Entities import task, taskState, taskSpec, taskSpecState
from Entities import san
from Entities import ran
from icent import IcentDemo
import servercheck


from TaskLanguage.checkGrammarTreeCreation import checkTaskLanguage
from TaskSupervisor.taskScheduler import taskScheduler
# from Entities import task.Task
# from Entities import taskstate.TaskState


def setup_logging(
    default_path='logging.json',
    default_level=logging.INFO,
    env_key='LOG_CFG'):
    """Setup logging configuration

    """
    path = default_path
    value = os.getenv(env_key, None)
    if value:
        path = value
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        logging.basicConfig(level=default_level)

setup_logging()
logger = logging.getLogger(__name__)
HOST = '0.0.0.0'
PORT = 5555
SERVER_ADDRESS = "localhost"


CONFIG_FILE = "./fiware_config.ini"
parsedConfigFile = Config(CONFIG_FILE)
#globals.initOcbHandler(parsedConfigFile.getFiwareServerAddress())
ocbHandler = globals.ocbHandler
# ContextBrokerHandler(parsedConfigFile.getFiwareServerAddress())
icentStateMachine = IcentDemo("Anda")
 
currenTaskDesc = task.Task()
# currentTaskState = taskState.TaskState("1a","2b", "3c")
currentTaskSpecState = taskSpecState.TaskSpecState()
ran_task_id = 0  
terminate = False 
    
import requests
import httplib

# todos: 
# updating the task id; actually HMI sets a task and the taskState represents a task
# taskLanguage
# stateMachine should be in charge of the states and dealing with the event; internal pub/sub mechanism
# shift method 'deleteSubscriptionById' to the context-broker; internal subscriptionId handler
# storage of subscriptions in a database, when starting the programm what to do with subscriptions (deleting? Adding a new name to it?);
# ending/exiting programm either by typing 'exit' or pushing ctrl-c
# json schema validation for this tools


#todo: put this into ran 
RAN_IS_DONE = 0
RAN_IS_MOVING = 1
RAN_IN_ACTION = 2

def deleteSubscriptionById(id):
    if(len(id)>1):
        try:
            logger.info("Deleting Subsciption: " + id) 
            #print parsedConfigFile.getFiwareServerAddress()+"/v2/subscriptions/"+ id
            response = requests.request("DELETE", parsedConfigFile.getFiwareServerAddress()+"/v2/subscriptions/"+ id)  
            if(response.status_code // httplib.OK == 1):
                logger.info("Unsubscribed: " + id) 
        except Exception as expression:
            logger.error("Failed Subsciption: " + id + expression) 
            return False
        return True

def signal_handler(sig, frame):
    global terminate
    terminate = True 
    logger.info('You pressed Ctrl+C!')
    logger.info("cleaning up")

    

def flaskThread(): 
    logger.info("Starting flaskServerThread")
    app.run(host= parsedConfigFile.FLASK_HOST, port= parsedConfigFile.TASKPLANNER_PORT, threaded=True,use_reloader=False, debug = True)

# def convertRanState(jsonReq):
#     loaded_r = (jsonReq['status_channel'])
#     loaded_r = loaded_r['value']
#     loaded_r = ldanke, oaded_r.replace("%27",'"')
#     d = json.loads(loaded_r)
#     return d


# def ranDealer(q):
#     global icentStateMachine
#     global ocbHandler
#     global currentTaskState
#     isMoving = False
#     while(True):
#         jsonReq, entityType = q.get()
#         jsonReq = jsonReq[0]
#         print "received RAN" 
#         if(entityType == "opil_v1.msg.RANState"):
#             # todo: check for state
#             d = None
#             if("status_channel" in jsonReq):
#                 d = convertRanState(jsonReq)
#                 global ran_task_id
#                 if (d["current_task_id"]["id"] != ran_task_id):
#                     print "change"
#                     print d["current_task_id"]["id"]
#                     print ran_task_id
#                 ran_task_id = d["current_task_id"]["id"]
#             if(d):
#                 if(d["ran_status"] == RAN_IS_MOVING):
#                     isMoving = True
#                 if(isMoving):
#                     # if a position of the AGV has reached do the following:
#                         # agv --> setActionMotion(Do nothing) and publish it
#                         # update taskState and publish it
#                         # change state of stateMachine
#                     if(icentStateMachine.state == "ran2LoadingDestination" and d["ran_status"]== RAN_IS_DONE):
#                         isMoving = False
#                         print "reached destination@Loading"         
#                         ocbHandler.update_entity_dirty(getActionChannel(d["current_task_id"]["id"]))
                         
#                         currentTaskState.state = taskState.State.Running
#                         currentTaskState.userAction = taskState.UserAction.WaitForLoading
#                         ocbHandler.update_entity(currentTaskState)

#                         # change state
#                         icentStateMachine.AgvArrivedAtLoadingDestination()
                        
#                     elif(icentStateMachine.state == "ran2UnloadingDestination" and d["ran_status"]==RAN_IS_DONE):
#                         isMoving = False
#                         print "reached destination@Unloading"            
#                         ocbHandler.update_entity_dirty(getActionChannel(d["current_task_id"]["id"]))

#                         currentTaskState.state = taskState.State.Running
#                         currentTaskState.userAction = taskState.UserAction.WaitForUnloading
#                         ocbHandler.update_entity(currentTaskState)

#                         icentStateMachine.AgvArrivedAtUnloadingDestination()
#                     elif(icentStateMachine.state == "ran2WaitingArea" and d["ran_status"]==RAN_IS_DONE):                    
#                         isMoving = False
#                         print "reached destination@Waiting"                        
#                         ocbHandler.update_entity_dirty(getActionChannel(d["current_task_id"]["id"]))    
#                         # perform transistin of state: Running --> Finished
#                         currentTaskState.state = taskState.State.Finished
#                         currentTaskState.userAction = taskState.UserAction.Idle
#                         ocbHandler.update_entity(currentTaskState) 
#                         # perform transistin of state: Finished --> Idle
#                         currentTaskState.state = taskState.State.Idle
#                         currentTaskState.userAction = taskState.UserAction.Idle
#                         ocbHandler.update_entity(currentTaskState)
#                         icentStateMachine.AgvArrivedAtWaitingArea() 

#                     print icentStateMachine.state

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
    logger.info("Setting up sanDealer")
    while True: 
        jsonReq, entityType = q.get() 
        #jsonReq = jsonReq[0]
        logger.info("Received json sanDealer, now continue")
        # if(entityType == "SensorAgent"):
        #     if(icentStateMachine.state == "wait4ran2loading"):
        #         # to do: check for SAN_ID, Type and Value
        #         # make sure this is a Switch Sensor and it is the value of 1
        #         readings = findSanById(jsonReq, "IR_1")
        #         if(readings):
        #             if(isButtonPressed(readings)):
        #                 currentTaskState.state = taskState.State.Running
        #                 currentTaskState.userAction = taskState.UserAction.Idle
        #                 ocbHandler.update_entity(currentTaskState) 

        #                 retVal = getMotionChannel(parsedConfigFile.unloadingArea)
        #                 ocbHandler.update_entity_dirty(retVal)                        
        #                 icentStateMachine.AgvIsLoaded()
        #                 print retVal
  
        #         # send agv to unload destination
        #         # todo: send agv to destinatin
        #     elif(icentStateMachine.state == "wait4ran2unloading"):
        #         # to do: check for SAN_ID, Type and Value
        #         readings = findSanById(jsonReq, "IR_2")
        #         if(readings):
        #             if(isButtonPressed(readings)):
        #                 currentTaskState.state = taskState.State.Running
        #                 currentTaskState.userAction = taskState.UserAction.Idle
        #                 ocbHandler.update_entity(currentTaskState) 
        #                 retVal = getMotionChannel(parsedConfigFile.waitingArea) # ATTENTION: NEED TO FIX THE LOCATION --> Waiting Area
        #                 ocbHandler.update_entity_dirty(retVal)
        #                 print retVal
        #                 # agv is unloaded manually and confirmed
        #                 icentStateMachine.AgvIsUnloaded()
        #         # send AGV to waiting area
        #     print icentStateMachine.state
        # else:
        #     print "Not a known Entitytype\n"
 
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

def taskSchedulerDealer(taskSchedulerQueue):
    
    logger.info("taskSchedulerDealer started")
    while True: 
        dmp = taskSchedulerQueue.get()
        ts = taskScheduler("feinfacherTest", dmp)
        ts.start()
        print "Is Running"
    
    logger.info("taskSchedulerDealer ended")        


def taskDealer(q):    
    global icentStateMachine  
    global currentTaskState
    global ocbHandler
    global currenTaskDesc
    global currentTaskSpecState
    
    logger.info("taskDealer started")
    while True: 
        jsonReq, entityType = q.get()
        jsonReq = jsonReq[0]
        logger.info("Received new TaskSpec")
        decodedString = jsonReq["TaskSpec"]["value"]
        decodedString = urllib.unquote_plus(decodedString)
        
        retVal, message = checkTaskLanguage(decodedString)
        currentTaskSpecState.message = str(message)
        if (retVal == 0): # no error
            logger.info("newTaskSpec:\n"+ str(decodedString))
            globals.taskSchedulerQueue.put(decodedString)
        
        currentTaskSpecState.state =  retVal
        currentTaskSpecState.refId = jsonReq["id"]
        ocbHandler.update_entity(currentTaskSpecState)
    
    logger.info("taskDealer ended")

        # if(entityType == "Task"):
        #     entityTask = task.Task() #taskState.getCurrentTaskId() 
        #     objectFiwareConverter.ObjectFiwareConverter.fiware2Obj(jsonReq,entityTask)
        #     if(icentStateMachine.state == "idle" and entityTask.taskId == currenTaskDesc.taskId and entityTask.state == task.TaskState.Start):
        #         if(entityTask.state == task.TaskState.Start):
        #             icentStateMachine.NewTask()
        #             currentTaskState.taskId = currenTaskDesc.taskId
        #             currentTaskState.state = taskState.State.Running
        #             currentTaskState.userAction = taskState.UserAction.Idle
        #             ocbHandler.update_entity(currentTaskState)
        #             # prepare of sending motionassignment tasks
        #             retVal = getMotionChannel(parsedConfigFile.loadingArea)
        #             ocbHandler.update_entity_dirty(retVal)
                    
        #             print icentStateMachine.state  
        #             #print render_template('./Templates.motion_channel.template',)
        #         # todo: Send AGV to LoadingDestination
        #     # elif(icentStateMachine.state == "error" and entityTask.state == task.TaskState.Reset):
                

        #     #     print icentStateMachine.state                        
        #     elif(entityTask.state== task.TaskState.EmergencyStop):
        #         # todo: stop the robot
        #         currentTaskState.taskId = currenTaskDesc.taskId
        #         currentTaskState.state = taskState.State.Aborted
        #         currentTaskState.userAction = taskState.UserAction.Idle
        #         currentTaskState.errorMessage = "Please reset the task"
        #         ocbHandler.update_entity(currentTaskState)
        #         icentStateMachine.Panic()
        #         print icentStateMachine.state

        #         currentTaskState.taskId = currenTaskDesc.taskId
        #         currentTaskState.state = taskState.State.Idle
        #         currentTaskState.userAction = taskState.UserAction.Idle
        #         currentTaskState.errorMessage = "Please restart the task"
        #         ocbHandler.update_entity(currentTaskState)
        #         icentStateMachine.Reset()

def obj2JsonArray(_obj):
    tempArray = []
    tempArray.append(_obj)
    print json.dumps(tempArray)
    return (tempArray)
 

def waitForEnd():
    logger.info("Starting waitForEnd")
    user_input = ""
    global terminate 
    while user_input!= "exit" or terminate==False:
        try:  
            user_input = input('Input please ?').strip('\n').strip('\r')
            if(user_input == "exit"):
                terminate = True
        except EOFError:
            pass
        except KeyboardInterrupt:
            print "ERR"
        except:
            global terminate
            terminate = False

if __name__ == '__main__': 
    global subscriptionDict
    global stateQueue 
    global ocbHandler
    global currenTaskDesc
    #global currentTaskState
    global currentTaskSpecState

 
    logger.info("Starting TaskPlanner")
    if(os.path.isfile('./images/task.png')):
        os.remove('./images/task.png')
    
    
    logger.info("Setting up Singal_Handler")
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)


    logger.info("Setting up checkIfServerIsUpRunning")
    checkIfServerIsUpRunning = threading.Thread(name='checkServerRunning', 
                                                target=servercheck.checkServerRunning, 
                                                args=(SERVER_ADDRESS, parsedConfigFile.TASKPLANNER_PORT,))

    logger.info("Setting up checkForProgrammEnd")
    checkForProgrammEnd = threading.Thread(name='waitForEnd', 
                                                target=waitForEnd, 
                                                args=())

    logger.info("Setting up flaskServerThread")
    flaskServerThread = threading.Thread(name= 'flaskThread',target = flaskThread) 

    checkIfServerIsUpRunning.start()       
     
    flaskServerThread.start() 
    print "wait for finish"
    checkIfServerIsUpRunning.join()
    # create an instance of the fiware ocb handler
    

    # few things commented due to the damn airplane mode 
    # publish first the needed entities before subscribing ot it
    ocbHandler.create_entity(currentTaskSpecState) 
    #ocbHandler.create_entity(currenTaskDesc) 

    # subscribe to entities

    #globals.subscriptionDict[subscriptionId] = task.Task.Type()
    subscriptionId = ocbHandler.subscribe2Entity( _description = "SAN Updates Notification",
            _entities = obj2JsonArray(san.San.getEntity()),  
            _notification = parsedConfigFile.getTaskPlannerAddress() +"/san",)     
    globals.subscriptionDict[subscriptionId] ="SensorAgent"       
     
      
    # subscriptionId = ocbHandler.subscribe2Entity( _description = "subscriber",
    #         _entities = obj2JsonArray(ran.Ran.getEntity()), _condition_attributes="status_channel",  
    #         _notification = parsedConfigFile.getTaskPlannerAddress()+"/ran",)
    # globals.subscriptionDict[subscriptionId] = "opil_v1.msg.RANState"             


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

    logger.info("Setting up taskDealer, sanDealer and workTaskScheduler")
    workerTask = Thread(target=taskDealer, args=(globals.taskQueue,))
    workerSan = Thread(target=sanDealer, args=(globals.sanQueue,))
    workerTaskScheduler = Thread(target=taskSchedulerDealer, args=(globals.taskSchedulerQueue,))
    #workerRan = Thread(target=ranDealer, args=(globals.ranQueue,))
    
    logger.info("Starting taskDealer, sanDealer and workTaskScheduler")
    workerTask.start()
    workerSan.start()
    workerTaskScheduler.start()
    #workerRan.start()
    
    subscriptionId = ocbHandler.subscribe2Entity( _description = "notify me",
            _entities = obj2JsonArray(taskSpec.TaskSpec.getEntity()),  
            _notification = parsedConfigFile.getTaskPlannerAddress() +"/task",_generic=True)
    globals.subscriptionDict[subscriptionId] ="TaskSpec"     

 
    # currentTaskState.taskId = taskState.getCurrentTaskId()
    # currentTaskState.state = taskState.State.Idle
    # currentTaskState.userAction = taskState.UserAction.Idle
    # ocbHandler.update_entity(currentTaskState)
 

    logger.info("Push Ctrl+C to exit()")


    # original_sigint = signal.getsignal(signal.SIGINT)
    # signal.signal(signal.SIGINT, original_sigint)

    # checkForProgrammEnd.start()
    # checkForProgrammEnd.join()

    while terminate == False:
        try:
            time.sleep(1)
        except Exception:
            pass        
        pass
    user_input = ""
    # while user_input!= "exit" or terminate==False:
    #     try:
    #         user_input = raw_input('Input please ?').strip('\n')
    #         user_input = user_input.replace('\r','')
    #     except KeyboardInterrupt:
    #         pass
    #     except:
    #         global terminate
    #         terminate = False

    logger.info("Shutting down TaskPlanner") 
    logger.info("Unsubscribing from Subscriptions")
    for item in globals.subscriptionDict:
        deleteSubscriptionById(item)
        
    logger.info("Unsubscribing from Subscriptions_done")
    
    logger.info("Deleting all created Entities")
    ocbHandler.shutDown()
    logger.info("Deleting all created Entities_done")

    # todo: delete subscriptions
    # ocbHandler.unregister_entities()
    # #SubscribtionHandler.unsubscribeContext(parsedConfigFile)

    logger.info("EndOf TaskPlanner")   
    os._exit(0)
