import logging
from collections import Counter

from globals import parsedConfigFile

logger = logging.getLogger(__name__)

indexRoundRobin = []
maxNumberPerRobot = []
robotOverview = {}


class Robot():
    def __init__(self, _id, _name, _type):
        self.id = _id
        self.name = _name
        self.type = _type

class RoundRobin():
    def __init__(self, _type):
        self.availableRobots = []
        self.currentIndex = 0
        self.type = _type
    
    def getNextRobot(self):
        robot = self.availableRobots[self.currentIndex]
        self.currentIndex += 1
        if(self.currentIndex >= len(self.availableRobots)):
            self.currentIndex = 0
        return robot
    
    def addRobot(self, _robot):
        exists = False
        for robot in self.availableRobots:
            if(robot.id == _robot.id):
                exists = True

        if(not exists):
            self.availableRobots.append(_robot)



def initRobot():
    global indexRoundRobin
    global robotOverview
    index = 0
    robotTypes = parsedConfigFile.robotTypes
    robots = parsedConfigFile.robots
    robotNames = parsedConfigFile.robotNames
    if(len(robotTypes) != len(robots) != len(robotNames)):
        return -1

    for robotType in robotTypes:
        robotType = robotType.lower()
        if(robotType not in robotOverview):
            tmpRoundRobin = RoundRobin(robotType)
            robotOverview[robotType] = tmpRoundRobin

        rbt= Robot(robots[index], robotNames[index], robotTypes[index])
        robotOverview[robotType].addRobot(rbt)
        index += 1

    # print("done")
    # print(getNextRobotByType("pallet"))
    # print(getNextRobotByType("pallet"))
    # print(getNextRobotByType("pallet"))

        
def getNextRobotByType(_type):
    global robotOverview
    if(_type not in robotOverview):
        return None

    rndRobin = robotOverview[_type]
    nextRobot = rndRobin.getNextRobot()
    print nextRobot
    return nextRobot

        



def getRobot(loadType):
    robotTypes = parsedConfigFile.robotTypes
    robots = parsedConfigFile.robots
    if(len(robotTypes) != len(robots)):
        return -1
    
    try:
        loadType = loadType.lower()
        index = robotTypes.index(loadType)
    
        if(index >=0 and index < len(robotTypes)):
            return robots[index]

    except:
        logger.info("Could not load a robot to the type" + str(loadType))
        return None    
        
    return None

    