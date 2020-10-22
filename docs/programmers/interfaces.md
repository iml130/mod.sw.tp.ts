# Interfaces 

In order to work as designed, the TaskSupervisor requires a Materialflow, which is specified on the TaskLanguage (Link)[]. This entity is explained below.

## Consuming

### Materialflow

* id : uuid
* type : Materialflow 
* specification : The materialflow needs to be described in format of [LotLan](https://lotlan.readthedocs.io/). The payload needs to be URL encoded - more information can be found [@w3schools.com](https://www.w3schools.com/tags/ref_urlencode.ASP)
* ownerId : Text (Reference to the static UUID of the instance for the HMI)
* active: Boolean (Indidicates, if the Materialflow shall be processed by the TaskSupervisor OR not. Important: ONCE the HMI shutsdown, the HMI *needs* to set the materialflow to disable. The User needs to enable it manually after an restart of the system. This is required that the system is not doing something unexpected after boot).

## Producing

### MaterialflowSpecificationState
This entity provides information about the Materialflow and the processed TaskLanguage.

* id : uuid
* type : MaterialflowSpecificationState
* message : String
* refId: String (reference to the Materialflow Entity)
* state: number (0 == ok, -1 ==  error, >0 == ok with some additional information (tbd))

### TransportOrderUpdate 
Once, a Transportion by an AGV starts, the TaskPlanner will create a TransportOrderUpdate. 

* id : uuid of the running instance
* type : TransportOrderUpdate
* pickupFrom : string (name of the pickup location)
* deliverTo : string (name of the delivery location)
* name : string (name of this task)
* refMaterialflowUpdateId : id (where has been this transportation defined)
* refOwnerId : id (who has this materialflow/transportation defined)
* taskInfo : int (Idle = 0, WaitForStartTrigger = 1, MovingToPickupDestination = 2, WaitForLoading = 3, MovingToDeliveryDestination = 4, WaitForUnloading = 5)
* updateTime : string (last update of this entity)
* startTime : string (when it has been started)
* robotId : string of the robot