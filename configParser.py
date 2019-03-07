import ConfigParser
import io
import sys

class Area(object):
    def __init(self):
        self.point_x = 0
        self.point_y = 0
        self.theta = 0

class Config(object):
    """description of class"""
    def __init__(self, _fileName):
        
        CONFIG_FILE = _fileName
        with open(CONFIG_FILE,'r+') as f:
            sample_config = f.read()
        config = ConfigParser.RawConfigParser(allow_no_value=True)
        config.readfp(io.BytesIO(sample_config))
        self.CB_HOST=config.get('contextbroker', 'host')
        self.CB_PORT=config.get('contextbroker', 'port')
        #self.CB_FIWARE_SERVICE=config.get('contextbroker', 'fiware_service')
        self.CB_FIWARE_SERVICEPATH = "/Sensors"
        self.CB_URL = "http://"+self.CB_HOST+":"+self.CB_PORT
        self.TASKPLANNER_PORT = int(config.get('taskplanner', 'port'))
        self.TASKPLANNER_HOST = config.get('taskplanner', 'host')
        
        #self.robot_id = config.get('RAN', 'robot_id')
        self.FLASK_HOST = config.get('flask', 'host')
        
        # self.loadingArea = Area()
        # self.loadingArea.point_x = config.get('loadingArea', 'point_x')
        # self.loadingArea.point_y = config.get('loadingArea', 'point_y')
        # self.loadingArea.theta  = config.get('loadingArea', 'theta')
        # self.waitingArea = Area()
        # self.waitingArea.point_x = config.get('waitingArea', 'point_x')
        # self.waitingArea.point_y = config.get('waitingArea', 'point_y')
        # self.waitingArea.theta  = config.get('waitingArea', 'theta')
        # self.unloadingArea = Area()
        # self.unloadingArea.point_x = config.get('unloadingArea', 'point_x')
        # self.unloadingArea.point_y = config.get('unloadingArea', 'point_y')
        # self.unloadingArea.theta  = config.get('unloadingArea', 'theta')

 
    def getTaskPlannerAddress(self):
        return "http://"+ self.TASKPLANNER_HOST + ":" + str(self.TASKPLANNER_PORT)
    def getFiwareServerAddress(self):
        return "http://"+ self.CB_HOST+":"+self.CB_PORT


