import uuid
class FiwareEntity():
    def __init__(self, id = None):
        self.type = self.__class__.__name__
        if(id is None):
            self.id = self.type + str(uuid.uuid4())
        else:
            self.id =self.type + str(id)  

    @classmethod
    def getEntity(cls):
        print cls.Type()
        print cls.Id()
        return { "id" : cls.Id() , "type" : cls.Type() }
    
    @classmethod
    def Id(cls):
        return cls.__name__+"1"

        
    @classmethod
    def Type(cls):
        return cls.__name__

    def getId(self):
        return self.id