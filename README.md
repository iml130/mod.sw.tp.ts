# TaskSupervisor



| :books: [Documentation](https://tte-project1.readthedocs.io/en/latest/) |
| --------------------------------------------- |

## Contents
* [Background](#Background)
* [Install](#Install)
* [Usage](#Usage)
* [API](#API)
* [Testing](#Testing)
* [License](#License)


## Background

The TaskSupervisor (TS) module receives materialflow specification from in an appropriate formal language (LoTLan) and parameterized task specification. The TS processes the received materialflow information and assigns the transport order to the available robots within the TaskSupervisor. The TaskSupervisor is also able to publish the current state of the transport order. Any changes inside the system will be handled through this module.

## Install

### Native
You have to do the following steps:
* Install requirements via pip
* Install ROS Noetic and create a [catkin workspace](http://wiki.ros.org/catkin/Tutorials/create_a_workspace)
* Install ROS-MARS
* Install [Orion](https://firos.readthedocs.io/en/latest/install/install.html)

### Docker Image

Alternatively we provide a [docker image](Docker/Dockerfile).

## Usage
You can start the TaskSupervisor by executing the [main file](tasksupervisor/__main__.py) via python.

## API

## Testing

## License
[APACHE2](LICENSE) ©