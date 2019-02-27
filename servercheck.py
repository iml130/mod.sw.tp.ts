import requests
import urllib2
import time
maxCheck = 100

### check if the server is running, otherwise wait until 
def checkServerRunning(SERVER_ADDRESS, PORT):
    doForever = True    
    maxCheckCounter = 0 
    while doForever:
        print "checkServerRunning"
        maxCheckCounter += 1
        if(maxCheckCounter == maxCheck):
            print "maxCheck is reached"
            doForever = False    
        try:
            tmpUrl = "http://"+ SERVER_ADDRESS+  ":" + str(PORT) 
            print "Try to access: " + tmpUrl
            request = urllib2.Request(tmpUrl) 
            response = urllib2.urlopen(request)        
            print "is working"
            doForever = False
        except urllib2.HTTPError, err:
            print('HTTPError = ' + str(err.code))
        except urllib2.URLError, err:
            print('URLError = ' + str(err.reason))
        except httplib.HTTPException, err:
            print('HTTPException')
        finally:
            time.sleep(100)
            print "FAILED"
    print "Thread is ending"
 
