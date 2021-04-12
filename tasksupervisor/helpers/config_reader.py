""" Contains ConfigReader class """

from os import path

import configparser

class ConfigReader(object):
    """ Object representation of an configuration ini file """

    def __init__(self, filename):

        CONFIG_FILE = filename

        if path.exists(filename):
            # with open(CONFIG_FILE, "r+") as f:
            #     sample_config = f.read()
            # config = configparser.RawConfigParser(allow_no_value=True)
            # config.readfp(io.BytesIO(sample_config))
            config = configparser.ConfigParser(inline_comment_prefixes="#")

            config.read(filename)
            self.CB_HOST = config.get("contextbroker", "host")
            self.CB_PORT = config.get("contextbroker", "port")
            #self.CB_FIWARE_SERVICE=config.get("contextbroker", "fiware_service")
            self.CB_FIWARE_SERVICEPATH = "/Sensors"
            self.CB_URL = "http://"+self.CB_HOST+":"+self.CB_PORT
            self.TASKPLANNER_PORT = int(config.get("taskplanner", "port"))
            self.TASKPLANNER_HOST = config.get("taskplanner", "host")

            #self.robot_id = config.get("RAN", "robot_id")
            self.FLASK_HOST = "0.0.0.0"

            self.robots = self._trim_array(
                config.get("robots", "ids").split(","))
            self.robot_types = self._trim_array(
                config.get("robots", "types").split(","))
            self.robot_names = self._trim_array(
                config.get("robots", "names").split(","))
        else:
            print("ERROR OPENING CONFIG FILE " + filename)
            raise OSError("Config File does not exists")

    def get_taskplanner_address(self):
        return "http://" + self.TASKPLANNER_HOST + ":" + str(self.TASKPLANNER_PORT)

    def get_fiware_server_address(self):
        return str("http://" + self.CB_HOST+":"+self.CB_PORT)

    def _trim_array(self, array):
        trimmed_array = []
        for item in array:
            if item:
                trimmed_array.append(item.strip().lower())
        return trimmed_array

    def is_valid(self):
        if len(self.robots) == 0:
            raise ValueError(
                "Please configure at least on robot (including id, type and name)")
        if(((len(self.robots) != len(self.robot_types)) or
            (len(self.robots) != len(self.robot_names))) or
            (len(self.robot_types) != len(self.robot_names))):
            raise ValueError(
                "Error with Robot Configutation; Missmatch with Ids, Names and Types")

        return True
