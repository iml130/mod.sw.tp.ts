import threading
import queue
import logging


logger = logging.getLogger(__name__)


class DictQueue:
    """ A thread safe dict queue having a single uuid-key in the dict """
    lock = threading.Lock()

    def __init__(self):
        logger.info("DictQueue init")
        self.dict = {}
        logger.info("DictQueue init_done")

    def addThread(self, _uuid):
        with self.lock:
            _uuid = str(_uuid)
            if _uuid in self.dict:
                return False
            self.dict[_uuid] = queue.Queue()
            logger.info("DictQueue UUID added: %s", _uuid)
            return True

    def getQueue(self, _uuid):
        with self.lock:
            _uuid = str(_uuid)
            if _uuid in self.dict:
                return self.dict[_uuid]
            return None

    def removeThread(self, _uuid):
        """ removes an uuid from the dict """
        with self.lock:
            _uuid = str(_uuid)
            if _uuid in self.dict:
                try:
                    del self.dict[_uuid]
                    logger.info("DictQueue UUID deleted: %s", _uuid)
                    return True
                except KeyError:
                    logger.error("DictQueue key not found: %s", _uuid)
                    return False
            return False

    def putData(self, _uuid, data):
        with self.lock:
            _uuid = str(_uuid)
            if _uuid in self.dict:
                q = self.dict[_uuid]
                q.put(data)
