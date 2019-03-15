import Queue

import threading

from helpers.dictQueue import DictQueue

from contextbrokerhandler import ContextBrokerHandler
from helpers.configParser import Config


taskQueue = Queue.Queue()
sanDictQueue = DictQueue()
sanQueue = Queue.Queue()
ranQueue = Queue.Queue()
taskSchedulerQueue = Queue.Queue()

subscriptionDict = {}

FI_SUB_ID = "subscriptionId"
FI_DATA = "data"

ocbHandler = None
CONFIG_FILE = "./fiware_config.ini"
parsedConfigFile = Config(CONFIG_FILE)
# globals.initOcbHandler(parsedConfigFile.getFiwareServerAddress())
ocbHandler = ContextBrokerHandler(parsedConfigFile.getFiwareServerAddress())

# def initOcbHandler(_address):
#     global ocbHandler
#     ocbHandler = ContextBrokerHandler(_address)
#     print "help"