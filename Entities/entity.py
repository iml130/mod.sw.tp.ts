class FiwareEntity():
    def __init__(self):
        self.type = self.__class__.__name__
        self.id = self.id + "1"

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
        return self.__class__.__name__+"1"