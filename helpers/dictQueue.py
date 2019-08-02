import threading
import Queue
import logging 


logger = logging.getLogger(__name__)

class DictQueue:
    lock = threading.Lock()

    def __init__(self):
        logger.info("DictQueue init")
        self.dict = {}
        logger.info("DictQueue init_done")

    def addThread(self, _uuid):
        with self.lock:
            _uuid = str(_uuid)
            if(_uuid in self.dict):
                return False
            self.dict[_uuid] = Queue.Queue()
            logger.info("DictQueue UUID added : " + _uuid)
            return True
    
    def getQueue(self, _uuid):
        with self.lock:
            _uuid = str(_uuid)
            if(_uuid in self.dict):
                return self.dict[_uuid]
            return None
    
    def removeThread(self, _uuid):
        with self.lock:
            _uuid = str(_uuid)
            if(_uuid in self.dict):
                try: 
                    del self.dict[_uuid]
                    logger.info("DictQueue UUID deleted : " + _uuid)
                    return True
                except KeyError:
                    logger.error("DictQueue key not found : " + _uuid)
                    return False
            return False
            
    def putData(self, _uuid, data):
        with self.lock:
            _uuid = str(_uuid)
            if(_uuid in self.dict):
                q = self.dict[_uuid]
                q.put(data)
    