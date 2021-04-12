""" Contains Materialflow API class """

import uuid

class Materialflow():
    def __init__(self):
        self.id = uuid.uuid4()
        self.specification = ""
        self.owner_id = ""
        self.active = False
        self.broker_ref_id = ""
