import ConfigParser
import io
import sys


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
        self.CB_FIWARE_SERVICE=config.get('contextbroker', 'fiware_service')
        self.CB_FIWARE_SERVICEPATH = "/Sensors"
        self.CB_URL = "http://"+self.CB_HOST+":"+self.CB_PORT
    

    def getFiwareServerAddress(self):
        return "http://"+ self.CB_HOST+":"+self.CB_PORT


