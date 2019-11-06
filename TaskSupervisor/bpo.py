import logging

from globals import parsedConfigFile

logger = logging.getLogger(__name__)

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

    