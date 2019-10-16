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
import requests
import httplib
from datetime import datetime 

# external lib imports
from flask import g 
from flask import render_template,Response
from jinja2 import Environment, FileSystemLoader

import rospy
from mars_agent_logical_msgs.msg import OrderStatus


# local imports
import globals 
from helpers.configParser import Config
from contextbrokerhandler import ContextBrokerHandler
from FiwareObjectConverter import objectFiwareConverter

from Entities import task 
from Entities.san import SensorAgent
from Entities import ran
from helpers.servercheck import checkServerRunning

from Entities.materialflow import Materialflow
from Entities.materialflowSpecificationSate import MaterialflowSpecificationState

from TaskLanguage.checkGrammarTreeCreation import checkTaskLanguage
from TaskSupervisor.schedular import Schedular

from tasksupervisor import TasksuperVisorInfo

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
    


#reconnect logging calls which are children of this to the ros log system

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
 
 
currenTaskDesc = task.Task()
listCurrentMaterialFlowSpecState = []
currentMaterialFlowSpecState = MaterialflowSpecificationState()
ran_task_id = 0  
terminate = False 
tsInfo = TasksuperVisorInfo()

# todos: 
# updating the task id; actually HMI sets a task and the taskState represents a task
# taskLanguage
# stateMachine should be in charge of the states and dealing with the event; internal pub/sub mechanism
# shift method 'deleteSubscriptionById' to the context-broker; internal subscriptionId handler
# storage of subscriptions in a database, when starting the programm what to do with subscriptions (deleting? Adding a new name to it?);
# ending/exiting programm either by typing 'exit' or pushing ctrl-c
  


def signal_handler(sig, frame):
    global terminate
    terminate = True 
    logger.info('You pressed Ctrl+C!')
    logger.info("cleaning up")

    
def flaskThread(): 
    logger.info("Starting flaskServerThread")
    app.run(host= parsedConfigFile.FLASK_HOST, port= parsedConfigFile.TASKPLANNER_PORT, threaded=True,use_reloader=False, debug = True)
 

def schedularDealer(schedularQueue):
    global tsInfo
    global ocbHandler
    ts = None
    logger.info("SchedularDealer started")
    threads = []
    while True: 
        ts = None
        dmp = schedularQueue.get()
        if(ts is None):
            ts = Schedular(dmp)
            ts.start()
            tsInfo.appendMaterielflow(dmp.id)
            ocbHandler.update_entity(tsInfo)
            #ts.join()
        else:
            print "Already running, not able to accept any others"
        print "Is Running"
    
    logger.info("SchedularDealer ended")        



def taskDealer(taskQueue): 

    lock = threading.Lock()
     
    global currentTaskState
    global ocbHandler
    global currenTaskDesc
    global listCurrentMaterialFlowSpecState
     
    
    logger.info("taskDealer started")
    while True: 
        jsonReq, entityType = taskQueue.get()
        with lock:
            for tempJsonReq in jsonReq:
               
                currentMaterialFlowSpecState = MaterialflowSpecificationState()
                objTaskSpec = Materialflow.CreateObjectFromJson(tempJsonReq)
                if(objTaskSpec.active): # check if the materialflow shall be processed - or not
                    retVal, message = checkTaskLanguage(objTaskSpec.specification)
                    currentMaterialFlowSpecState.message = message
                    if(retVal == 0):
                        logger.info("newTaskSpec:\n"+ str(objTaskSpec.specification))
                        globals.taskSchedulerQueue.put(objTaskSpec)
            
                    currentMaterialFlowSpecState.message = message
                    currentMaterialFlowSpecState.state = retVal
                    currentMaterialFlowSpecState.refId = tempJsonReq["id"]
                    retVal = ocbHandler.create_entity(currentMaterialFlowSpecState)
                    if(retVal == 0):
                        listCurrentMaterialFlowSpecState.append(currentMaterialFlowSpecState)
                else:
                    print("TODO: Disable the Materialflow or ignore it...but first... lets make it easy")
        #ocbHandler.update_entity(currentMaterialFlowSpecState)
    
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
    global currentMaterialFlowSpecState

    logger.info("Subscriptions to /order_status")
    

    logger.info("Setting up ROS")
    rospy.init_node('task_supervisor' ) 
    rospy.Subscriber("/order_status", OrderStatus, callback_ros_order_state)
    setup_logging()

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
    retVal = ocbHandler.create_entity(tsInfo) 
    if (retVal == 0):   
        logger.info("Orion Connection is working - created TaskSpecState Entity")
        logger.info("Orion Address: " + parsedConfigFile.getFiwareServerAddress())



    logger.info("Setting up taskDealer, sanDealer and workTaskScheduler")
    workerTask = Thread(target=taskDealer, args=(globals.taskQueue,)) 
    workerTaskScheduler = Thread(target=schedularDealer, args=(globals.taskSchedulerQueue,)) 
    
    logger.info("Starting taskDealer, sanDealer and workTaskScheduler")
    workerTask.start() 
    workerTaskScheduler.start() 
    
    objMaterialflow = Materialflow()
    subscriptionId = ocbHandler.subscribe2Entity( _description = "Materialflow subscription",
            _entities = objMaterialflow.obj2JsonArray(),  
            _notification = parsedConfigFile.getTaskPlannerAddress() +"/task",_generic=True)
    globals.subscriptionDict[subscriptionId] ="Materialflow"     
  

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
  
