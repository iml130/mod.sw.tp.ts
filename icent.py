from transitions import Machine
import random

class IcentDemo(object):

    # Define some states. Most of the time, narcoleptic superheroes are just like
    # everyone else. Except for...
    states = ['init', 'idle', 'ran2loading', 'wait4ran2loading', 'ran2unloading', 'ran2waitingarea', 'finished', 'error']

    def __init__(self, name):

        # No anonymous superheroes on my watch! Every narcoleptic superhero gets
        # a name. Any name at all. SleepyMan. SlumberGirl. You get the idea.
        self.name = name
 
        # Initialize the state machine
        self.machine = Machine(model=self, states=IcentDemo.states, initial='idle')

        # Add some transitions. We could also define these using a static list of
        # dictionaries, as we did with states above, and then pass the list to
        # the Machine initializer as the transitions= argument.

        # At some point, every superhero must rise and shine.
        self.machine.add_transition(trigger='start', source='idle', dest='ran2loading')

        # Superheroes need to keep in shape.
        self.machine.add_transition(trigger='Go2LoadingArea', source='ran2loading', dest='wait4ran2loading')

        
        self.machine.add_transition('panic', '*', 'error')
        self.machine.add_transition('init', 'error', 'idle')

    def update_journal(self):
        """ Dear Diary, today I saved Mr. Whiskers. Again. """
        self.kittens_rescued += 1

    def is_exhausted(self):
        """ Basically a coin toss. """
        return random.random() < 0.5

    def change_into_super_secret_costume(self):
        print("Beauty, eh?")