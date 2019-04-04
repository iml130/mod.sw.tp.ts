__author__ = "Peter Detzner" 
__maintainer__ = "Peter Detzner"
__version__ = "0.0.1a"
__status__ = "Developement"

# system imports
import signal
import sys
import os
import urllib
from sys import exit
from os import environ
from setup import app
import logging
import logging.config
import time
import urllib2
import threading
from threading import Event, Thread
from Queue import Queue
import json

# external lib imports
from flask import g 
from flask import render_template,Response

from datetime import datetime 
from jinja2 import Environment, FileSystemLoader

import rospy
from mars_agent_logical_msgs.msg import OrderStatus


# local imports
import globals 
from helpers.configParser import Config
from contextbrokerhandler import ContextBrokerHandler
from FiwareObjectConverter import objectFiwareConverter

from Entities import task, taskState, taskSpec, taskSpecState

from Entities.san import SensorAgent
from Entities import ran
from icent import IcentDemo
from helpers.servercheck import checkServerRunning

from Entities.taskSpec import TaskSpec
from TaskLanguage.checkGrammarTreeCreation import checkTaskLanguage
from TaskSupervisor.taskScheduler import taskScheduler

from ROS.OrderState import OrderState, rosOrderStatus
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
if(parsedConfigFile.FLASK_HOST):
    PORT = int(parsedConfigFile.TASKPLANNER_PORT)
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


def signal_handler(sig, frame):
    global terminate
    terminate = True 
    logger.info('You pressed Ctrl+C!')
    logger.info("cleaning up")

    
def flaskThread(): 
    logger.info("Starting flaskServerThread")
    app.run(host= parsedConfigFile.FLASK_HOST, port= parsedConfigFile.TASKPLANNER_PORT, threaded=True,use_reloader=False, debug = True)

# def findSanById(_sensorData, _id):
#     for sensorArrayItem in _sensorData:

#         for sensorData in sensorArrayItem['sensorData']['value']:
             
#             if(sensorData['sensorType']['value'] == "IR Sensor" and sensorData['sensorId']['value'] == _id):
#                 return sensorData['readings']['value']

# def isButtonPressed(values):
#     for reading in values:
#         if(reading['reading']['value'] == True):
#             return True
#     return False 

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
 
# def getActionChannel(task_id):
#     j2_env = Environment(loader=FileSystemLoader("./Templates"), trim_blocks=True)
#     retVal = j2_env.get_template('action_channel.template').render(robot_id = parsedConfigFile.robot_id, task_id=task_id)
#     retVal = retVal.replace('\t', '').replace('\n', '')
#     return retVal

# def getMotionChannel(area):
#     j2_env = Environment(loader=FileSystemLoader("./Templates"), trim_blocks=True)
#     new_task_id = ran_task_id
#     # if(new_task_id > 1):
#     #     new_task_id += 1
#     retVal = j2_env.get_template('motion_channel.template').render(area=area, robot_id = parsedConfigFile.robot_id, task_id=new_task_id)
#     retVal = retVal.replace('\t', '').replace('\n', '')
#     return retVal

def taskSchedulerDealer(taskSchedulerQueue):
    ts = None
    logger.info("taskSchedulerDealer started")
    while True: 
        
        dmp = taskSchedulerQueue.get()
        if(ts is None):
            ts = taskScheduler("feinfacherTest", dmp)
            ts.start()
        else:
            print "Already running, not able to accept any others"
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
    
        objTaskSpec = TaskSpec.CreateObjectFromJson(jsonReq)

        retVal, message = checkTaskLanguage(objTaskSpec.TaskSpec)
        currentTaskSpecState.message = message
        if(retVal == 0):
            logger.info("newTaskSpec:\n"+ str(objTaskSpec.TaskSpec))
            globals.taskSchedulerQueue.put(objTaskSpec.TaskSpec)
 
        currentTaskSpecState.message = message
        currentTaskSpecState.state = retVal
        currentTaskSpecState.refId = jsonReq["id"]
        ocbHandler.update_entity(currentTaskSpecState)
    
    logger.info("taskDealer ended")
 

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

def callback_ros_order_state(data):
    #rospy.loginfo(data.order_id)  
    os  = OrderState.CreateObjectRosMsg(data)
    if(os):
        if(os.status == rosOrderStatus.FINISHED):
            logger.info("Received callback_ros_order_state --> FIN")
        globals.rosMessageDispatcher.putData(os.uuid,os)
           
            
if __name__ == '__main__': 
    global subscriptionDict
    global stateQueue 
    global ocbHandler
    global currenTaskDesc
    #global currentTaskState
    global currentTaskSpecState

    logger.info("Setting up ROS")
    rospy.init_node('task_supervisor') 
    
    logger.info("Subscriptions to /order_status")
    rospy.Subscriber("/order_status", OrderStatus, callback_ros_order_state)

    logger.info("Starting TaskPlanner")
    if(os.path.isfile('./images/task.png')):
        os.remove('./images/task.png')
    
    
    logger.info("Setting up Singal_Handler")
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler) 


    logger.info("Setting up checkIfServerIsUpRunning")
    checkIfServerIsUpRunning = threading.Thread(name='checkServerRunning', 
                                                target=checkServerRunning, 
                                                args=(SERVER_ADDRESS, parsedConfigFile.TASKPLANNER_PORT,))

    logger.info("Setting up checkForProgrammEnd")
    checkForProgrammEnd = threading.Thread(name='waitForEnd', 
                                                target=waitForEnd, 
                                                args=())

    logger.info("Setting up flaskServerThread")
    flaskServerThread = threading.Thread(name= 'flaskThread',target = flaskThread) 

    checkIfServerIsUpRunning.start()       
     
    flaskServerThread.start() 
    logger.info("Starting Flask and wait")
    checkIfServerIsUpRunning.join()
    logger.info("Flask is running")
    # create an instance of the fiware ocb handler
    

    # few things commented due to the damn airplane mode 
    # publish first the needed entities before subscribing ot it
    retVal = ocbHandler.create_entity(currentTaskSpecState) 
    if (retVal == 0):
        logger.info("Orion Connection is working - created TaskSpecState Entity")
        logger.info("Orion Address: " + parsedConfigFile.getFiwareServerAddress())
    #ocbHandler.create_entity(currenTaskDesc) 

    # subscribe to entities

    #globals.subscriptionDict[subscriptionId] = task.Task.Type()
    # subscriptionId = ocbHandler.subscribe2Entity( _description = "SAN Updates Notification",
    #         _entities = obj2JsonArray(san.San.getEntity()),  
    #         _notification = parsedConfigFile.getTaskPlannerAddress() +"/san",)     
    # globals.subscriptionDict[subscriptionId] ="SensorAgent"       
     
      
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
    #workerSan = Thread(target=sanDealer, args=(globals.sanQueue,))
    workerTaskScheduler = Thread(target=taskSchedulerDealer, args=(globals.taskSchedulerQueue,))
    #workerRan = Thread(target=ranDealer, args=(globals.ranQueue,))
    
    logger.info("Starting taskDealer, sanDealer and workTaskScheduler")
    workerTask.start()
    #workerSan.start()
    workerTaskScheduler.start()
    #workerRan.start()
    
    objTaskSpec = TaskSpec()
    subscriptionId = ocbHandler.subscribe2Entity( _description = "notify me",
            _entities = objTaskSpec.obj2JsonArray(),  
            _notification = parsedConfigFile.getTaskPlannerAddress() +"/task",_generic=True)
    globals.subscriptionDict[subscriptionId] ="TaskSpec"     
  

    logger.info("Push Ctrl+C to exit()")
 

    while terminate == False:
        try:
            time.sleep(1)
        except Exception:
            pass        
        pass
    user_input = "" 

    
    # clean up means, delete 
    #   - all subscriptions
    #   - all created entities

    logger.info("Shutting down TaskPlanner") 
    logger.info("Unsubscribing from Subscriptions")
    # TODO: error with threads, size of dict might change:
    # better: get keys and iterate overy keys
    for subId in globals.subscriptionDict:
        ocbHandler.deleteSubscriptionById(subId)
        
    logger.info("Unsubscribing from Subscriptions_done")
    
    logger.info("Deleting all created Entities")
    ocbHandler.shutDown()
    logger.info("Deleting all created Entities_done")

 
    logger.info("EndOf TaskPlanner")   
    os._exit(0)
