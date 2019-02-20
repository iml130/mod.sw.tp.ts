import threading
import time 
from random import randint
import uuid 
import Queue

from globals import sanDictQueue

from transportOrder import TransportOrder

class Task(threading.Thread):
    def __init__(self, _name):
        threading.Thread.__init__(self) 
        self.uuid = uuid.uuid1()      
        self.name = _name
        sanDictQueue.addThread(self.uuid)
        self.q = sanDictQueue.getQueue(self.uuid)
        #self.transportOrder = TransportOrder(self.name)

    def __str__(self):
        return self.name    
     
    def __repr__(self):
        return self.__str__()

    def run(self):   
        tempVal = (randint(2,7))
        print "SpawnTaskToken: " + str(self.uuid)
        print "\nrunning " + self.name + ", sleep " + str(tempVal)
        #time.sleep(tempVal)
        try:
            a = self.q.get(timeout = 60)
            if (a):
                print "Received:" +str(a)
        except Queue.Empty:
            pass
        sanDictQueue.removeThread(self.uuid)
        print "finished now " + self.name

