""" Contains MaterialflowSpecification Fiware class """

from tasksupervisor.endpoint.fiware_orion.entities.entity import FiwareEntity

class MaterialflowSpecificationState(FiwareEntity):
    """ This entity provides information about the Materialflow and the processed TaskLanguage. """
    def __init__(self):
        FiwareEntity.__init__(self)
        self.refId = ""
        self.state = SpecState.Idle
        self.message = ""

    @classmethod
    def from_api_object(cls, api_mf_spec_state):
        mf_spec_state = MaterialflowSpecificationState()

        mf_spec_state.id = str(api_mf_spec_state.id)
        mf_spec_state.refId = api_mf_spec_state.ref_id
        mf_spec_state.state = api_mf_spec_state.state
        mf_spec_state.message = api_mf_spec_state.message

        return mf_spec_state

# TASK
# 0= No-Task, 1 = Start, 2 = Pause, 3 = Cancel, 4 = EmergencyStop, 5 = Reset"
# TASK_STATE
# Idle : 0, Running : 1, Waiting : 2, Active : 3, Finished : 4, Aborted : 5, Error : 6


class SpecState():
    Idle = 0
    Ok = 1
    Error = -1
