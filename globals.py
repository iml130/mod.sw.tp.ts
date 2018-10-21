import Queue

import threading

taskQueue = Queue.Queue()
sanQueue = Queue.Queue()
ranQueue = Queue.Queue()

subscriptionDict = {}

FI_SUB_ID = "subscriptionId"
FI_DATA = "data"
