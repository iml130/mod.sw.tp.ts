# Overview TP

The two  main functional building blocks like the Task Supervisor (TS) and the Motion Task Planning (MTP) will be described in this section.
Task Supervisor

The Task Supervisor (TS) module receives task specification from the HMI Module in an appropriate formal language and parameterized task specification. The TS process the received task information and assigns transport order to the available Robots. The Task Supervisor is also able to send the current state information to the HMI. Any changes inside the system will be handled through this sub-module.
Motion Task Planning

The submodule Motion Task Planner (MTP) of the Task Planner (TP) is a software module as part of OPIL (Open Platform for Innovation in Logistics). The MTP modules creates/computes a motion task plan for the involved agents. This motion task provides a deadlock-free, optimal or near optimal path without loops and collision. Beyond this path computation the Motion Task Planning component handles the communication with the Agents. 