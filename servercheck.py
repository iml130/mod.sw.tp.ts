import requests
import urllib2
import httplib
import logging

maxCheck = 100

logger = logging.getLogger(__name__)

### check if the server is running, otherwise wait until 
def checkServerRunning(SERVER_ADDRESS, PORT):
    doForever = True    
    maxCheckCounter = 0 
    while doForever: 
        logger.info("CheckServerRunning, retry "+ str(maxCheckCounter) + "/" + str(maxCheck))
        maxCheckCounter += 1
        if(maxCheckCounter == maxCheck):
            logger.info("CheckServerRunning maximum retries reached") 
            doForever = False    
        try:
            tmpUrl = "http://"+ SERVER_ADDRESS+  ":" + str(PORT) 
            logger.info("CheckServerRunning Try to access: " + tmpUrl) 
      
            request = urllib2.Request(tmpUrl) 
            response = urllib2.urlopen(request)        
            logger.info("CheckServerRunning is avalable " + tmpUrl) 
            doForever = False
        except urllib2.HTTPError, err:
            logger.error("CheckServerRunning HTTPError" + str(err.code)) 
        except urllib2.URLError, err:
            logger.error("CheckServerRunning URLError" + str(err.code)) 
        except httplib.HTTPException, err:
            logger.error("CheckServerRunning HTTPException" + str(err.code)) 
        finally: 
            logger.error("CheckServerRunning Failed") 
    logger.info("CheckServerRunning_done") 
 
