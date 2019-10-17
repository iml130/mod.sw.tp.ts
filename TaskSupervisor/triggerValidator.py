import ast 
import logging

logger = logging.getLogger(__name__)


COMPARISON_OPERATOR_EQUAL = "=="
COMPARISON_OPERATOR_NOT_EQUAL = "!="
COMPARISON_OPERATOR_LESS_THAN = "<"
COMPARISON_OPERATOR_GREATER_THAN = ">"
COMPARISON_OPERATOR_LESS_OR_EQUAL_THAN = "<="
COMPARISON_OPERATOR_GREATER_OR_EQUAL_THAN = ">="

def validateTrigger(expectedType, sensorData, trigger):
    retVal, actualType = checkForType(expectedType, sensorData)
    if retVal:
        return checkForValue(actualType, sensorData, trigger)
        # expected value is true, now check if the real value is also correct

def checkForValue(actualType, realValue, trigger):
    
    receivedValue = realValue[0]["reading"]
    #receivedValue = False
    triggerValue = trigger["right"]
    print type(triggerValue)
    print ast.literal_eval(triggerValue)
    compareOperator = trigger["binOp"]
    logger.info("receivedValue: " + str(receivedValue) + ", expectedValue: " + str(triggerValue))

    if(actualType >= 0 and actualType <=2 ):
        # 0 = boolean, 1 = integer, 2 = float
        retVal = False 
        if(compareOperator == COMPARISON_OPERATOR_EQUAL): # equal
            retVal = (ast.literal_eval(triggerValue) == receivedValue)
        elif(compareOperator == COMPARISON_OPERATOR_GREATER_THAN): # greater               
            retVal = (receivedValue > ast.literal_eval(triggerValue))
        elif(compareOperator == COMPARISON_OPERATOR_LESS_THAN): # less than      
            retVal = (receivedValue > ast.literal_eval(triggerValue))
        elif(compareOperator == COMPARISON_OPERATOR_GREATER_OR_EQUAL_THAN): # greater than or equal
            retVal = (receivedValue >= ast.literal_eval(triggerValue))
        elif(compareOperator == COMPARISON_OPERATOR_LESS_OR_EQUAL_THAN): # less than or equal
            retVal = (receivedValue <= ast.literal_eval(triggerValue)) 
        elif(compareOperator == COMPARISON_OPERATOR_NOT_EQUAL): # not euqal
            retVal = (ast.literal_eval(triggerValue) != receivedValue) 
        return retVal 
        # boolean
    
    elif(actualType == 3):
        # str
        pass
    pass

def checkForType(expectedType, sensorData):
    expectedType = expectedType.lower()
    sensorReadingType = sensorData[0]["reading"]
    if(expectedType == "boolean" or expectedType == "bool"):
        if(isinstance(sensorReadingType, bool)):
            logger.info("ExpectedType: " + expectedType + ", receivedType: Bool")
            return True, 0
    elif(expectedType == "integer" or expectedType == "int"):
        if(isinstance(sensorReadingType, (long, int))):
            logger.info("ExpectedType: " + expectedType + ", receivedType: Integer")
            return True, 1
    elif(expectedType == "float"):
        if(isinstance(sensorReadingType,float)):
            logger.info("ExpectedType: " + expectedType + ", receivedType: Float")
            return True, 2
    elif(expectedType == "str"):
        if(isinstance(sensorReadingType, str)):
            logger.info("ExpectedType: " + expectedType + ", receivedType: Str")
            return True,3
    return False, None

 