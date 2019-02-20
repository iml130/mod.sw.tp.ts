import threading
import Queue

class DictQueue:
    lock = threading.Lock()

    def __init__(self):
        self.dict = {}
    
    def addThread(self, _uuid):
        with self.lock:
            _uuid = str(_uuid)
            if(_uuid in self.dict):
                return False
            self.dict[_uuid] = Queue.Queue()
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
                    print "UUID deleted: " + _uuid
                    return True
                except KeyError:
                    print("Key 'testing' not found")
                    return False
            return False
            
    def putData(self, _uuid, data):
        with self.lock:
            _uuid = str(_uuid)
            if(_uuid in self.dict):
                q = self.dict[_uuid]
                q.put(data)