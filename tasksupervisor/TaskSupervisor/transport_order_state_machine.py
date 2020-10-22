from transitions import Machine
import random
import uuid
from enum import Enum


# maybe it would be better to inject the received data/events to the statemachine of icent
# as parameter ocb handler would be required (including concurency, m)
# a singleton-task-generator also to store the latest information
# configuration file (first: hardcoded, later config file)
#
def createUuid(salt):
    return uuid.uuid3(uuid.NAMESPACE_URL, salt)


class TRANSPORT_ORDER_STATES(Enum):
    INIT = 0
    WAIT_FOR_TRIGGER = 1
    START_PICKUP = 2
    MOVING_TO_PICKUP = 3
    WAITING_FOR_LOADING = 4
    START_DELIVERY = 5
    MOVING_TO_DELIVERY = 6
    WAITING_FOR_UNLOADING = 7
    WAIT_FOR_FINISHED = 8
    WAIT_FOR_FINISHED_EVENTS = 9
    FINISHED = 10
    ERROR = 11


class TransportOrderStateMachine(object):

    # Define some states. Most of the time, narcoleptic superheroes are just like
    # everyone else. Except for...
    states = ['init', 'waitForTrigger', 'startPickup', 'movingToPickup', 'waitForLoading', 'startDelivery',
              'movingToDelivery', 'waitForUnloading', 'waitForFinished', 'waitForFinishedEvents', 'finished', 'error']

    def __init__(self, name):
        self.name = name
        #self.task = task
        self.uuid = createUuid(self.name)
        print(self.uuid)
        # Initialize the state machine
        self.machine = Machine(
            model=self, states=TransportOrderStateMachine.states, initial='init')
        self.machine.add_ordered_transitions()
        # Add some transitions. We could also define these using a static list of
        # dictionaries, as we did with states above, and then pass the list to
        # the Machine initializer as the transitions= argument.

        # At some point, every superhero must rise and shine.
        self.machine.add_transition(
            trigger='Initialized', source='init', dest='waitForTrigger')
        self.machine.add_transition(
            trigger='TriggerReceived', source='waitForTrigger', dest='startPickup')


# Pickup
        self.machine.add_transition(
            trigger='GotoPickupDestination', source='startPickup', dest='movingToPickup')

        self.machine.add_transition(
            trigger='ArrivedAtPickupDestination', source='movingToPickup', dest='waitForLoading')
        self.machine.add_transition(
            trigger='AgvIsLoaded', source='waitForLoading', dest='startDelivery')

# Delivery
        self.machine.add_transition(trigger='GotoDeliveryDestination',
                                    source='startDelivery', dest='movingToDelivery')

        self.machine.add_transition(trigger='ArrivedAtDeliveryDestination',
                                    source='movingToDelivery', dest='waitForUnloading')

        self.machine.add_transition(
            trigger='AgvIsUnloaded', source='waitForUnloading', dest='waitForFinished')

# Unused at the moment
        self.machine.add_transition(
            trigger='OrderStart', source='moveOrderStart', dest='moveOrder')
        self.machine.add_transition(
            trigger='OrderFinished', source='moveOrder', dest='moveOrderFinished')
# Done
        self.machine.add_transition(
            trigger='SubscribedToFinishedEvents', source='waitForFinished', dest='waitForFinishedEvents')

        self.machine.add_transition(
            trigger='FinishedTriggerReceived', source='waitForFinishedEvents', dest='finished')

        self.machine.add_transition(
            trigger='FinishedReceived', source=['waitForFinished','waitForFinishedEvents'], dest='finished')

        self.machine.add_transition(
            trigger='TransportOrderError', source='*', dest='error')

        self.machine.add_transition(trigger='Panic', source='*', dest='idle')
        self.machine.add_transition('Panic', '*', 'error')
        self.machine.add_transition('Init', 'error', 'init')

    # def registerForTrigger(self):
    #     print "reigstererd for Trigger"

    def get_state(self):
        return self.state

    def current_state_is(self, _state):
        if not isinstance(_state, TRANSPORT_ORDER_STATES):
            raise RuntimeError("Wrong parameter")
        if self.__dict__["state"]:
            if self.state == self.states[_state.value]:
                return True
        return False

    def getUuid(self):
        return self.uuid


if __name__ == "__main__":
    to_state = TransportOrderStateMachine("peter")
    print(to_state.current_state_is(234))
    print(to_state.current_state_is(TRANSPORT_ORDER_STATES.INIT))
    print(to_state.current_state_is(TRANSPORT_ORDER_STATES.WAIT_FOR_TRIGGER))
