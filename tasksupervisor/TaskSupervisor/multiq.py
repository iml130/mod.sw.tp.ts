"""
Contains MultiQueue class
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


class QueueReader(threading.Thread):
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


class MultiQueue(queue.Queue):
    """ Allow multiple queues to be waited upon """
    def __init__(self, list_of_queues):
        queue.Queue.__init__(self)
        self.q_list = list_of_queues
        self.qr_list = []
        for q in list_of_queues:
            qr = QueueReader(q, self)
            qr.start()
            self.qr_list.append(qr)

    def get(self, blocking=True, timeout=None):
        res = []
        while len(res) == 0:
            if len(self.q_list) == 0:
                res = (self, EndOfQueueMarker)
            else:
                res = queue.Queue.get(self, blocking, timeout)
                if res[1] is EndOfQueueMarker:
                    self.q_list.remove(res[0])
                    res = []
        return res

    def join(self):
        for qr in self.qr_list:
            qr.join()

    def finish(self):
        for qr in self.q_list:
            qr.put(EndOfQueueMarker)
        self.join()


def select(list_of_queues):
    outq = queue.Queue()
    for q in list_of_queues:
        qr = QueueReader(q, outq)
        qr.start()
    return outq.get()
