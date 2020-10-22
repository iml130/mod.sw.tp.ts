Our sample configuration *config_ts.ini* defines two robots, having the same skill transporting *pallets*. The assignment of tasks is done by a simple round-robin shedulling algorithm. This means, task1 is assigned to robot1, task2 is assigned to robot2. Task3 is assigned to robot1, and so on. In case of a third robot exists, task3 would have been assigned to this on.

2 Robots with ids:
- robot_00000000000000000000000000000101
- robot_00000000000000000000000000000100

These ids are also published during the TransportOrderUpdate by the TaskSupervisor.

```ini
[taskplanner]
; hostname or ip address of the TaskPlanner machine 
; Please note that "tp" in docker-compose.yml must match
host = infacts.ts
; Port of the task planner
PORT = 2906

[contextbroker]
; hostname or ip address of the context broker machine 
; Please note that "orion" in docker-compose.yml must match
host= orion
; Port of the context broker
port=1026

[robots]
ids = robot_00000000000000000000000000000101,   robot_00000000000000000000000000000100
# Capabilities can be self defined in TL under Location -> Type
# E.g.: 
# Location dropoffItem
#     name = "ws1_dropoff"
#     type = "SmallLoadCarrier"
# end
types = pallet, pallet
# Names of the robots
names = ztf1, ztf2
```
