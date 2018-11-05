import requests
import urllib2

maxCheck = 5

### check if the server is running, otherwise wait until 
def checkServerRunning(SERVER_ADDRESS, PORT):
    doForever = True    
    maxCheckCounter = 0 
    while doForever:
        print "checkServerRunning"
        if(maxCheckCounter == maxCheck):
            doForever = False    
        try:
            request = urllib2.Request("http://"+ SERVER_ADDRESS+  ":" + str(PORT) ) 
            response = urllib2.urlopen(request)        
            doForever = False
        except urllib2.HTTPError, err:
            print('HTTPError = ' + str(err.code))
        except urllib2.URLError, err:
            print('URLError = ' + str(err.reason))
        except httplib.HTTPException, err:
            print('HTTPException')
        else:
            print "FAILED"
    print "Thread is ending"
 