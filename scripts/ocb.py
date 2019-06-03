
__author__ = "ptrdtznr"
__status__ = "Dev"


NGSI_VERSION_V2 = "v2"
OCB_SERVER_ADDRESS = "localhost"
OCB_POST = "1026"

SUBSCRIPTIONS = "subscriptions"
ENTITIES = "entities"

def getAddress(specific = ""):
    
    address = "http://" + OCB_SERVER_ADDRESS + ":" + OCB_POST + "/" + NGSI_VERSION_V2 + "/" + specific
    if len(specific):
        address = address + "/"
    return address
