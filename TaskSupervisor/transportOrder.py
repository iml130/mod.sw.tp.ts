from transitions import Machine
import random
import uuid


# maybe it would be better to inject the received data/events to the statemachine of icent
# as parameter ocb handler would be required (including concurency, m)
# a singleton-task-generator also to store the latest information
# configuration file (first: hardcoded, later config file)
#
def createUuid(salt):
    return uuid.uuid3(uuid.NAMESPACE_URL, salt)

class TransportOrder(object):

    # Define some states. Most of the time, narcoleptic superheroes are just like
    # everyone else. Except for...
    states = ['init', 'waitForTrigger', 'moveOrderStart', 'moveOrder', 'moveOrderFinished', 'finished', 'error']
    
    def __init__(self, name):
        self.name = name
        #self.task = task
        self.uuid = createUuid(self.name)
        print self.uuid
        # Initialize the state machine
        self.machine = Machine(model=self, states=TransportOrder.states, initial='init')
        self.machine.add_ordered_transitions()
        # Add some transitions. We could also define these using a static list of
        # dictionaries, as we did with states above, and then pass the list to
        # the Machine initializer as the transitions= argument.

        # At some point, every superhero must rise and shine.
        self.machine.add_transition(trigger='Initialized', source='init', dest='waitForTrigger')
        self.machine.add_transition(trigger='TriggerReceived', source='waitForTrigger', dest='moveOrderStart') 
        self.machine.add_transition(trigger='OrderStart', source='moveOrderStart', dest='moveOrder') 
        self.machine.add_transition(trigger='OrderFinished', source='moveOrder', dest='moveOrderFinished') 
        self.machine.add_transition(trigger='DestinationReached', source='moveOrderFinished', dest='finished')

        self.machine.add_transition(trigger='Panic', source='*', dest='idle')
        self.machine.add_transition('Panic', '*', 'error')
        self.machine.add_transition('Init', 'error', 'init')

    # def registerForTrigger(self):
    #     print "reigstererd for Trigger"

    def getUuid(self):
        return self.uuid
