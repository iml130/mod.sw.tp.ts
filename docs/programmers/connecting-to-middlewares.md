It is possible to connect the TaskSupervisor to different middlewares, in fact you can receive your materialflow specification for example via [MQTT](https://mqtt.org/), [FIWAREs Orion Context Broker](https://github.com/telefonicaid/fiware-orion) and send the control command towards any other middlewars or systems, e.g. like the Robot Operating System [ROS](https://www.ros.org/).

At the moment we support only FIWAREs Orion Context Broker (OCB) and ROS1. But in the future, we are going to be open as much as possible. We will present open interfaces so that it will be possible to interconnect everything. 


ORION <-> TaskSupervisor <-> ROS