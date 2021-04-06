import sys
import queue
import threading

from tasksupervisor.helpers.dict_queue import DictQueue
from tasksupervisor.helpers.config_reader import ConfigReader

# Receives all the message and forwards it
rosMessageDispatcher = DictQueue()


taskQueue = queue.Queue()
# Handling the temporary SAN EPs
sanDictQueue = DictQueue()

sanQueue = queue.Queue()
ranQueue = queue.Queue()
taskSchedulerQueue = queue.Queue()

lock = None
if lock is None:
    lock = threading.Lock()
subscriptionDict = {}

FI_SUB_ID = "subscriptionId"
FI_DATA = "data"

ORION_CONNECTOR = None
CONFIG_FILE = "./tasksupervisor/fiware_config.ini"
try:
    parsed_config_file = ConfigReader(CONFIG_FILE)
    parsed_config_file.is_valid()
except Exception:
    sys.exit(0)
