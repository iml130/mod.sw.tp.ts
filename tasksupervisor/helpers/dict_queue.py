""" Contains DictQueue class """

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

    def add_thread(self, uuid):
        with self.lock:
            uuid = str(uuid)
            if uuid in self.dict:
                return False
            self.dict[uuid] = queue.Queue()
            logger.info("DictQueue UUID added: %s", uuid)
            return True

    def get_queue(self, uuid):
        with self.lock:
            uuid = str(uuid)
            if uuid in self.dict:
                return self.dict[uuid]
            return None

    def remove_thread(self, uuid):
        """ removes an uuid from the dict """
        with self.lock:
            uuid = str(uuid)
            if uuid in self.dict:
                try:
                    del self.dict[uuid]
                    logger.info("DictQueue UUID deleted: %s", uuid)
                    return True
                except KeyError:
                    logger.error("DictQueue key not found: %s", uuid)
                    return False
            return False

    def put_data(self, uuid, data):
        with self.lock:
            uuid = str(uuid)
            if uuid in self.dict:
                q = self.dict[uuid]
                q.put(data)
