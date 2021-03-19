import uuid

class Materialflow():
    def __init__(self, id=uuid.uuid4()):
        self.id = id
        self.specification = ""
        self.owner_id = ""
        self.active = False
