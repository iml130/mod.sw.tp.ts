""" Contains MaterialflowSpecificationState and SpecState API class """

import uuid

class MaterialflowSpecificationState():
    """ This entity provides information about the Materialflow and the processed TaskLanguage. """
    def __init__(self):
        self.id = uuid.uuid4()
        self.ref_id = ""
        self.state = SpecState.Idle
        self.message = ""
        self.broker_ref_id = ""

# TASK
# 0= No-Task, 1 = Start, 2 = Pause, 3 = Cancel, 4 = EmergencyStop, 5 = Reset"
# TASK_STATE
# Idle : 0, Running : 1, Waiting : 2, Active : 3, Finished : 4, Aborted : 5, Error : 6

class SpecState():
    Idle = 0
    Ok = 1
    Error = -1
