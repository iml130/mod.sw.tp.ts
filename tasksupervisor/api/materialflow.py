import uuid

class Materialflow():
    def __init__(self, id=uuid.uuid4()):
        self.id = id
        self.specification = ""
        self.ownerId = ""
        self.active = False