# TaskSupervisor



| :books: Documentation |
| --------------------------------------------- |

## Contents
* [Background](#Background)
* [OpenToDo's](#OpenTodo's)
* [Prerequisites](#Prerequisites)
* [Install](#Install)
* [Usage](#Usage)
* [API](#API)
* [Testing](#Testing)
* [License](#License)


## Background

[OPIL](https://opil-documentation.readthedocs.io/) is the Open Platform for Innovations in Logistcs. This platform is meant to enable the development of value added services for the logistics sector in small-scale Industry 4.0 contexts such as those of manufacturing SMEs. In fact, it provides an easy deployable suite of applications for rapid development of complete logistics solutions, including components for task scheduling, path planning, automatic factory layout generation and navigation.

This module is part of the TaskPlanner (TP). TP is one of the three OPIL Components and Functional blocks which this 3rd Layer (mod.sw.tp) is made of. Regarding the OPIL architecture, this node consists of two different sub-modules:

Firstly, the Task Supervisor (mod.sw.tp.ts) monitors the execution of the task dispatched to the agents (Robots). Secondly, the Motion Task Planning (mod.sw.tp.mtp) plans the motion tasks for the robot agents. Task Planner makes it possible for the different components to communicate with each other and be composed into full-fledged logistic system in a manufacturing environment.

Receives material flow specification from in an appropriate formal language (LoTLan) and parameterized task specification. The TS processes the received material flow information and assigns the transport order to the available robots within the TaskSupervisor. The TaskSupervisor is also able to publish the current state of the transport order. Any changes inside the system will be handled through this module.

## Prerequisites
* Python3 >= 3.8.5
* ROS1 Noetic
* (Docker and docker-compose - in case you want to have an easy life ;))
* Understanding defining material flows based on [lotlan](https://lotlan.readthedocs.io/en/latest/)

## OpenTodo's
Currently we are working on the following topics. It takes some time.
* Documentation preparation
* Interface abstraction to be independent of brokers
* Some heuristics for choosing the next AGV

## Install
This module can be used either via a native usage or via docker. It is up to you!

### Native
You have to do the following steps:
* Install requirements via pip
```
pip install -r requirements.txt
```
* Install ROS Noetic and create a [catkin workspace](http://wiki.ros.org/catkin/Tutorials/create_a_workspace)
* TODO: git clone repo
```
cd catkin_ws/src
git clone repo
```
* Install ROS-MARS
* Install [FIWARE Orion Context Broker](https://fiware-orion.readthedocs.io/en/master/) via [Docker](https://hub.docker.com/r/fiware/orion/)


## Configuration

This modules requires a [configuration file](docs/install/configuration.md).


### Docker Image

Alternatively we provide a [docker image](Docker/Dockerfile).

## Usage Native
* Start Orion
* Start ROS-MARS
```
cd catkin_ws/src/mod.sw.tp.ts
python __main__.py
```

## API
[Consumed interfaces](docs/programmers/interfaces.md#Consuming)

[Produced interfaces](docs/programmers/interfaces.md#Producing)

## Testing
Comming soon

## License
[APACHE2](LICENSE) ©
