from transitions import Machine
import random



# maybe it would be better to inject the received data/events to the statemachine of icent
# as parameter ocb handler would be required (including concurency, m)
# a singleton-task-generator also to store the latest information
# configuration file (first: hardcoded, later config file)
#

class IcentDemo(object):

    # Define some states. Most of the time, narcoleptic superheroes are just like
    # everyone else. Except for...
    states = ['init',  'reset', 'idle', 'ran2LoadingDestination', 'wait4ran2loading', 'ran2UnloadingDestination',
              'wait4ran2unloading', 'ran2WaitingArea', 'finished', 'error']

    def __init__(self, name):

        self.name = name
 
        # Initialize the state machine
        self.machine = Machine(model=self, states=IcentDemo.states, initial='idle')

        # Add some transitions. We could also define these using a static list of
        # dictionaries, as we did with states above, and then pass the list to
        # the Machine initializer as the transitions= argument.

        # At some point, every superhero must rise and shine.
        self.machine.add_transition(trigger='NewTask', source='idle', dest='ran2LoadingDestination', after=self.update_journal)
        self.machine.add_transition(trigger='AgvArrivedAtLoadingDestination', source='ran2LoadingDestination', dest='wait4ran2loading')
        self.machine.add_transition(trigger='AgvIsLoaded', source='wait4ran2loading', dest='ran2UnloadingDestination')
        self.machine.add_transition(trigger='AgvArrivedAtUnloadingDestination', source='ran2UnloadingDestination', dest='wait4ran2unloading')
        self.machine.add_transition(trigger='AgvIsUnloaded', source='wait4ran2unloading', dest='ran2WaitingArea')
        self.machine.add_transition(trigger='AgvArrivedAtWaitingArea', source='ran2WaitingArea', dest='idle')
        
        self.machine.add_transition('Panic', '*', 'error')
        self.machine.add_transition('Reset', 'error', 'idle')
        self.machine.add_transition('Init', ['reset','error'], 'idle')

    def update_journal(self):
        """ Dear Diary, today I saved Mr. Whiskers. Again. """
        print "update journal"

    def is_exhausted(self):
        """ Basically a coin toss. """
        return random.random() < 0.5

    def change_into_super_secret_costume(self):
        print("Beauty, eh?")