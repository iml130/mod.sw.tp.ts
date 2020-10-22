"""
Allow multiple queues to be waited upon.

An EndOfQueueMarker marks a queue as
    "all data sent on this queue".
When this marker has been accessed on
all input threads, this marker is returned
by the multi_queue.

based on: https://stackoverflow.com/questions/1123855/select-on-multiple-python-multiprocessing-queues
"""
import queue
import threading


class EndOfQueueMarker:
    def __str___(self):
        return "End of data marker"
    pass


class queue_reader(threading.Thread):
    def __init__(self, inq, sharedq):
        threading.Thread.__init__(self)
        self.inq = inq
        self.sharedq = sharedq

    def run(self):
        q_run = True
        while q_run:
            data = self.inq.get()
            result = (self.inq, data)
            self.sharedq.put(result)
            if data is EndOfQueueMarker:
                q_run = False


class multi_queue(queue.Queue):
    def __init__(self, list_of_queues):
        queue.Queue.__init__(self)
        self.qList = list_of_queues
        self.qrList = []
        for q in list_of_queues:
            qr = queue_reader(q, self)
            qr.start()
            self.qrList.append(qr)

    def get(self, blocking=True, timeout=None):
        res = []
        while len(res) == 0:
            if len(self.qList) == 0:
                res = (self, EndOfQueueMarker)
            else:
                res = queue.Queue.get(self, blocking, timeout)
                if res[1] is EndOfQueueMarker:
                    self.qList.remove(res[0])
                    res = []
        return res

    def join(self):
        for qr in self.qrList:
            qr.join()

    def finish(self):
        for qr in self.qList:
            qr.put(EndOfQueueMarker)
        
        self.join()


def select(list_of_queues):
    outq = queue.Queue()
    for q in list_of_queues:
        qr = queue_reader(q, outq)
        qr.start()
    return outq.get()
