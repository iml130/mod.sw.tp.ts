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
    states = ['init', 'idle', 'waitForTrigger', 'goToPosA', "atPosAArived","goToPosB", "atPosBArived", 'finished', 'error']
    
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
        self.machine.add_transition(trigger='Init', source='init', dest='idle', after='registerForTrigger')
        self.machine.add_transition(trigger='SubscribeToTrigger', source='idle', dest='waitForTrigger', before='registerForTrigger')
        self.machine.add_transition(trigger='GoToA', source='waitForTrigger', dest='goToPosA')
        self.machine.add_transition(trigger='AtPosAArived', source='goToPosA', dest='atPosAArived')
        self.machine.add_transition(trigger='GoToB', source='atPosAArived', dest='goToPosB')
        self.machine.add_transition(trigger='AtPosBArived', source='goToPosB', dest='atPosBArived')
        self.machine.add_transition(trigger='Finished', source='atPosBArived', dest='finished')
        self.machine.add_transition(trigger='Panic', source='*', dest='idle')
        self.machine.add_transition('Panic', '*', 'error')
        self.machine.add_transition('Init', 'error', 'init')

    def registerForTrigger(self):
        print "reigstererd for Trigger"

    def getUuid(self):
        return self.uuid
