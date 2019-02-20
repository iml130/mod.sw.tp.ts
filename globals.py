import Queue

import threading

from dictQueue import DictQueue

taskQueue = Queue.Queue()
sanDictQueue = DictQueue()
sanQueue = Queue.Queue()
ranQueue = Queue.Queue()
taskSchedulerQueue = Queue.Queue()

subscriptionDict = {}

FI_SUB_ID = "subscriptionId"
FI_DATA = "data"
