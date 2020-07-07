import io
import sys
import os.path
from os import path

import ConfigParser


class Config(object):
    """description of class"""

    def __init__(self, _fileName):

        CONFIG_FILE = _fileName

        if(path.exists(_fileName)):
            with open(CONFIG_FILE, 'r+') as f:
                sample_config = f.read()
            config = ConfigParser.RawConfigParser(allow_no_value=True)
            config.readfp(io.BytesIO(sample_config))
            self.CB_HOST = config.get('contextbroker', 'host')
            self.CB_PORT = config.get('contextbroker', 'port')
            #self.CB_FIWARE_SERVICE=config.get('contextbroker', 'fiware_service')
            self.CB_FIWARE_SERVICEPATH = "/Sensors"
            self.CB_URL = "http://"+self.CB_HOST+":"+self.CB_PORT
            self.TASKPLANNER_PORT = int(config.get('taskplanner', 'port'))
            self.TASKPLANNER_HOST = config.get('taskplanner', 'host')

            #self.robot_id = config.get('RAN', 'robot_id')
            self.FLASK_HOST = "0.0.0.0"

            self.robots = self._trimArray(
                config.get("robots", "ids").split(","))
            self.robotTypes = self._trimArray(
                config.get("robots", "types").split(","))
            self.robotNames = self._trimArray(
                config.get("robots", "names").split(","))
        else:
            print("ERROR OPENING CONFIG FILE " + _fileName)
            raise OSError("Config File does not exists")

    def getTaskPlannerAddress(self):
        return "http://" + self.TASKPLANNER_HOST + ":" + str(self.TASKPLANNER_PORT)

    def getFiwareServerAddress(self):
        return "http://" + self.CB_HOST+":"+self.CB_PORT

    def _trimArray(self, _array):
        trimmedArray = []
        for item in _array:
            if(len(item)):
                trimmedArray.append(item.strip().lower())
        return trimmedArray

    def isValid(self):
        if(len(self.robots) == 0):
            raise StandardError(
                "Please configure at least on robot (including id, type and name)")
        if((len(self.robots) != len(self.robotTypes)) or (len(self.robots) != len(self.robotNames))) or (len(self.robotTypes) != len(self.robotNames)):
            raise StandardError("Error with Robot Configutation; Missmatch with Ids, Names and Types")

        return True
