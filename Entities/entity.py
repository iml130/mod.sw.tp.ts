import uuid
class FiwareEntity():
    def __init__(self, id = None):
        self.type = self.__class__.__name__
        if(id is None):
            self.id = self.type + str(uuid.uuid4())
        else:
            self.id =self.type + str(id)  
 
    def getEntity(self): 
        print "Create Entity: id: " + self.getId() + ", type: " + self.getType()
        
        return { "id" : self.getId() , "type" : self.getType() }
    
      
    def getType(self):
        return self.type

    def getId(self):
        return self.id
    
    def obj2JsonArray(self):
        tempArray = []
        tempArray.append(self.getEntity())
         
        return (tempArray)