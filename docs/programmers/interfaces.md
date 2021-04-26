# Interfaces 

In order to work as designed, the TaskSupervisor requires a Materialflow, which is specified in the [TaskLanguage](https://lotlan.readthedocs.io/en/latest/index.html). Besides there are other entities that give important information. All entities which are used by the *TaskSupervisor* are explained below.

## Consuming

### Materialflow

* id : uuid
* specification : The materialflow needs to be described in format of [LotLan](https://lotlan.readthedocs.io/). The payload needs to be URL encoded - more information can be found [@w3schools.com](https://www.w3schools.com/tags/ref_urlencode.ASP)
* ownerId : Text (Reference to the static UUID of the instance for the HMI)
* active: Boolean (Indidicates, if the Materialflow shall be processed by the TaskSupervisor OR not. Important: ONCE the HMI shutsdown, the HMI *needs* to set the materialflow to disable. The User needs to enable it manually after an restart of the system. This is required that the system is not doing something unexpected after boot).

### SensorAgent
Represents a physical sensor

* id: uuid
* measurement_type: String
* modified_time: String in ISO8601 format
* reading: List of SensorData
* san_id: String
* sensor_id: String
* sensor_manufacturer: String
* sensor_type: String (ON-OFF sensor, ..)
* units: String (unit of measurement)
* broker_ref_id: uuid of the broker interface the corresponding materialflow is from

### SensorData

* readings: List of readings (for example True or False by an ON_OFF sensor)

## Producing

### TaskSupervisorInfo
Gets created at the start of the Supervisor and provides information about the total number of started materialflows

* id: uuid
* used_materialflows: List of started materialflows
* number_of_materialflows: int, length of used_materialflows
* message: String

### MaterialflowSpecificationState
This entity provides information about the Materialflow and the processed TaskLanguage.

* id : uuid
* message : String
* ref_id: String (reference to the Materialflow Entity)
* state: number (0 == ok, -1 ==  error, >0 == ok with some additional information (tbd))
* broker_ref_id: uuid of the broker interface the corresponding materialflow is from

### MaterialflowUpdate
Gets created when a Materialflow starts to run

* id: uuid
* task_manager_name:
* transport_order_list:
* ref_owner_id:
* time: String in utc format
* broker_ref_id: uuid of the broker interface the corresponding materialflow is from

### TransportOrderUpdate 
Once, a Transportion by an AGV starts, the TaskPlanner will create a TransportOrderUpdate. 

* id : uuid of the running instance
* pickup_from : String (name of the pickup location)
* deliver_to : String (name of the delivery location)
* name : String (name of this task)
* ref_materialflow_update_id : id (where has been this transportation defined)
* ref_owner_id : id (who has this materialflow/transportation defined)
* task_info : int (Idle = 0, WaitForStartTrigger = 1, MovingToPickupDestination = 2, WaitForLoading = 3, MovingToDeliveryDestination = 4, WaitForUnloading = 5)
* update_time : String (last update of this entity)
* start_time : String (when it has been started)
* robot_id : String of the robot
* broker_ref_id: uuid of the broker interface the corresponding materialflow is from